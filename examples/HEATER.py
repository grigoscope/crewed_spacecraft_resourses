import time
from HEATED_PWM import HEATER
import board

# Инициализация нагревателя с использованием пинов
heater = HEATER(pin1=board.IO21, pin2=board.IO47)

while True:
        # Установить нагрев на 30%
        print("Устанавливаем нагрев на 30%")
        heater.SetHeat(30)
        time.sleep(10)

        # Установить нагрев на 0%
        print("Устанавливаем нагрев на 100%")
        heater.SetHeat(0)
        time.sleep(100)