import math
import struct
from time import sleep
from busio import I2C, SPI
from digitalio import DigitalInOut

from I2C_SPI_protocol_Base import I2C_Impl

_BMP280_ADDRESS = 0x77
_BMP280_CHIPID = 0x58
_BMP280_REGISTER_CHIPID = 0xD0

OVERSCAN_X1 = 0x01
OVERSCAN_X16 = 0x05

_BMP280_MODES = [0x00, 0x01, 0x03]

STANDBY_TC_125 = 0x02  # 125ms

MODE_SLEEP = 0x00
MODE_FORCE = 0x01
MODE_NORMAL = 0x03

_BMP280_REGISTER_SOFTRESET = 0xE0
_BMP280_REGISTER_CTRL_HUM = 0xF2
_BMP280_REGISTER_STATUS = 0xF3
_BMP280_REGISTER_CTRL_MEAS = 0xF4
_BMP280_REGISTER_CONFIG = 0xF5
_BMP280_REGISTER_TEMPDATA = 0xFA

class Adafruit_BMP280:
    def __init__(self, bus_implementation: I2C_Impl) -> None:
        # Check device ID.
        self._bus_implementation = bus_implementation
        chip_id = self._read_byte(_BMP280_REGISTER_CHIPID)
        if _BMP280_CHIPID != chip_id:
            raise RuntimeError("Failed to find BMP280! Chip ID 0x%x" % chip_id)
        # Set some reasonable defaults.
        self._iir_filter = 0
        self.overscan_humidity = OVERSCAN_X1
        self.overscan_temperature = OVERSCAN_X1
        self.overscan_pressure = OVERSCAN_X16
        self._t_standby = STANDBY_TC_125
        self._mode = MODE_NORMAL
        self._reset()
        self._read_coefficients()
        self._write_ctrl_meas()
        self._write_config()
        self.sea_level_pressure = 1013.25
        """Pressure in hectoPascals at sea level. Used to calibrate `altitude`."""
        self._t_fine = None

    """         Shared    """
    def temperature(self) -> float:
        """The compensated temperature in degrees Celsius."""
        self._read_temperature()
        return self._t_fine / 5120.0
    
    def pressure(self) -> float:
        """
        The compensated pressure in hectoPascals.
        """
        self._read_temperature()
        # https://github.com/BoschSensortec/BMP280_driver/blob/master/BMP280.c
        adc = (
            self._read24(0xF7) / 16  # BMP280_REGISTER_PRESSUREDATA
        )  # lowest 4 bits get dropped
        var1 = float(self._t_fine) / 2.0 - 64000.0
        var2 = var1 * var1 * self._pressure_calib[5] / 32768.0
        var2 = var2 + var1 * self._pressure_calib[4] * 2.0
        var2 = var2 / 4.0 + self._pressure_calib[3] * 65536.0
        var3 = self._pressure_calib[2] * var1 * var1 / 524288.0
        var1 = (var3 + self._pressure_calib[1] * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self._pressure_calib[0]
        if not var1:  # avoid exception caused by division by zero
            raise ArithmeticError(
                "Invalid result possibly related to error while reading the calibration registers"
            )
        pressure = 1048576.0 - adc
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = self._pressure_calib[8] * pressure * pressure / 2147483648.0
        var2 = pressure * self._pressure_calib[7] / 32768.0
        pressure = pressure + (var1 + var2 + self._pressure_calib[6]) / 16.0

        pressure /= 1000 # /1000-kPa or /100-hPa
        return pressure
    
    def altitude(self) -> float:
        """The altitude based on current :attr:`pressure` versus the sea level pressure
        (``sea_level_pressure``) - which you must enter ahead of time)"""
        pressure = self.pressure()  # in Si units for hPascal
        return 44330 * (1.0 - math.pow(pressure / self.sea_level_pressure, 0.1903))

    def get_mode(self) -> int:
        return self._mode

    def set_mode(self, value: int) -> None:
        if not value in _BMP280_MODES:
            raise ValueError("Mode '%s' not supported" % (value))
        self._mode = value
        self._write_ctrl_meas()
        
    """         Private    """
    def _read_temperature(self) -> None:
        # perform one measurement
        if self.get_mode() != MODE_NORMAL:
            self.set_mode(MODE_FORCE)
            # Wait for conversion to complete
            while self._get_status() & 0x08:
                sleep(0.002)
        raw_temperature = (
            self._read24(_BMP280_REGISTER_TEMPDATA) / 16
        )  # lowest 4 bits get dropped

        var1 = (
            raw_temperature / 16384.0 - self._temp_calib[0] / 1024.0
        ) * self._temp_calib[1]

        var2 = (
            (raw_temperature / 131072.0 - self._temp_calib[0] / 8192.0)
            * (raw_temperature / 131072.0 - self._temp_calib[0] / 8192.0)
        ) * self._temp_calib[2]

        self._t_fine = int(var1 + var2)

    def _reset(self) -> None:
        """Soft reset the sensor"""
        self._write_register_byte(_BMP280_REGISTER_SOFTRESET, 0xB6)
        sleep(0.01)  # Datasheet 2ms.  

    def _write_ctrl_meas(self) -> None:
        """
        Write the values to the ctrl_meas and ctrl_hum registers in the device
        ctrl_meas sets the pressure and temperature data acquisition options
        ctrl_hum sets the humidity oversampling and must be written to first
        """
        self._write_register_byte(_BMP280_REGISTER_CTRL_HUM, self.overscan_humidity)
        self._write_register_byte(_BMP280_REGISTER_CTRL_MEAS, self._ctrl_meas())

    def _get_status(self) -> int:
        """Get the value from the status register in the device"""
        return self._read_byte(_BMP280_REGISTER_STATUS)

    def _read_config(self) -> int:
        """Read the value from the config register in the device"""
        return self._read_byte(_BMP280_REGISTER_CONFIG)

    def _write_config(self) -> None:
        """Write the value to the config register in the device"""
        normal_flag = False
        if self._mode == MODE_NORMAL:
            # Writes to the config register may be ignored while in Normal mode
            normal_flag = True
            self.set_mode(MODE_SLEEP)  # So we switch to Sleep mode first
        self._write_register_byte(_BMP280_REGISTER_CONFIG, self._config())
        if normal_flag:
            self.set_mode(MODE_NORMAL)

    def _config(self) -> int:
        """Value to be written to the device's config register"""
        config = 0
        if self.get_mode() == 0x03:  # MODE_NORMAL
            config += self._t_standby << 5
        if self._iir_filter:
            config += self._iir_filter << 2
        return config

    def _ctrl_meas(self) -> int:
        """Value to be written to the device's ctrl_meas register"""
        ctrl_meas = self.overscan_temperature << 5
        ctrl_meas += self.overscan_pressure << 2
        ctrl_meas += self.get_mode()
        return ctrl_meas

    def _read_coefficients(self) -> None:
        """Read & save the calibration coefficients"""
        coeff = self._read_register(0x88, 24)  # BMP280_REGISTER_DIG_T1
        coeff = list(struct.unpack("<HhhHhhhhhhhh", bytes(coeff)))
        coeff = [float(i) for i in coeff]
        self._temp_calib = coeff[:3]
        self._pressure_calib = coeff[3:]

        self._humidity_calib = [0] * 6
        self._humidity_calib[0] = self._read_byte(0xA1)  # BMP280_REGISTER_DIG_H1
        coeff = self._read_register(0xE1, 7)  # BMP280_REGISTER_DIG_H2
        coeff = list(struct.unpack("<hBbBbb", bytes(coeff)))
        self._humidity_calib[1] = float(coeff[0])
        self._humidity_calib[2] = float(coeff[1])
        self._humidity_calib[3] = float((coeff[2] << 4) | (coeff[3] & 0xF))
        self._humidity_calib[4] = float((coeff[4] << 4) | (coeff[3] >> 4))
        self._humidity_calib[5] = float(coeff[5])

    def _read_byte(self, register: int) -> int:
        """Read a byte register value and return it"""
        return self._read_register(register, 1)[0]

    def _read24(self, register: int) -> float:
        """Read an unsigned 24-bit value as a floating point and return it."""
        ret = 0.0
        for b in self._read_register(register, 3):
            ret *= 256.0
            ret += float(b & 0xFF)
        return ret

    def _read_register(self, register: int, length: int) -> bytearray:
        return self._bus_implementation.read_register(register, length)

    def _write_register_byte(self, register: int, value: int) -> None:
        self._bus_implementation.write_register_byte(register, value)


class Adafruit_BMP280_I2C(Adafruit_BMP280):
    def __init__(self, i2c: I2C, address: int = 0x77) -> None:  # BMP280_ADDRESS
        super().__init__(I2C_Impl(i2c, address))

# class Adafruit_BMP280_SPI(Adafruit_BMP280):
#     def __init__(self, spi: SPI, cs: DigitalInOut, baudrate: int = 100000) -> None:
#         super().__init__(SPI_Impl(spi, cs, baudrate))
