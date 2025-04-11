import pwmio
import digitalio
from microcontroller import Pin

class HEATER:
    
    # H-bridge specification
    # xIN1 | xIN2 |  FUNCTION
    # PWM  | 0    | Forward PWM, fast decay
    # 1    | PWM  | Forward PWM, slow decay
    # 0    | PWM  | Reverse PWM, fast decay
    # PWM  | 1    | Reverse PWM, slow decay

    ################################### Setup

    def __init__(self, pin1: Pin, pin2: Pin):
        # Initialize motor control pins
        self.xIN1 = pin1
        self.xIN2 = pin2

        # Set up xIN1 as a PWM output with initial duty cycle of 0 and frequency of 50Hz
        self.xIN1 = pwmio.PWMOut(pin=self.xIN1, duty_cycle=0, frequency=50)

        # Set up xIN2 as a digital output
        self.xIN2 = digitalio.DigitalInOut(self.xIN2)
        self.xIN2.direction = digitalio.Direction.OUTPUT

    def __del__(self):
        # Clean up resources when the object is deleted
        try:
            self.xIN1.deinit()
        except Exception:
            pass
        try:
            self.xIN2.deinit()
        except Exception:
            pass

    def SetHeat(self, heat):
        # Heat control 0 ... 100 %
        # Calculate duty cycle based on speed
        duty = heat * 20000.0 / 100.0

        # Set xIN2 value based on direction
        self.xIN2.value = True if heat > 0 else False

        # Update PWM duty cycle
        self.xIN1.duty_cycle = int(duty)