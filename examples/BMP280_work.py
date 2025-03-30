import board
import time
import busio
from lib import BMP280

################################### Настройка
# начальная задержка
time.sleep(1)
# Создаем объект модуля i2c
i2c1_module = busio.I2C(scl=board.IO2, sda=board.IO3)
# Создаем объект bmp280
bmp280      = BMP280.Adafruit_BMP280_I2C(i2c1_module, BMP280._BMP280_ADDRESS)
# Устанавливаем давление на уровне моря
bmp280.sea_level_pressure = 101.325 # кПа

################################### Работа
while True:
    # Получаем данные с устройства
    temp    = bmp280.temperature()
    press   = bmp280.pressure()
    alt     = bmp280.altitude()

    # выводим
    print(f"\nТемпература   : {temp} C")
    print(f"Давление      : {press} кПа")
    print(f"Высота        : {alt} метров")
    time.sleep(2)