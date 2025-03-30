import board
import time

from lib import SERVO

################################### Настройка
# Серво 1
PWM1_pin = board.IO48
# Серво 2
PWM2_pin = board.IO45
# Серво 3 - общий с МОТОРОМ B
PWM3_pin = board.IO42
# Серво 4 - общий с МОТОРОМ B
PWM4_pin = board.IO41

servo1 = SERVO.SERVO(PWM1_pin)  # Инициализация серво 1
servo2 = SERVO.SERVO(PWM2_pin)  # Инициализация серво 2
################################### Работа
while True:
    time.sleep(1)  # Задержка 1 секунда
    servo1.ServoSetAngle(0)  # Установить угол серво 1 в 0 градусов
    servo2.ServoSetAngle(180)  # Установить угол серво 2 в 180 градусов
    time.sleep(1)  # Задержка 1 секунда
    servo1.ServoSetAngle(180)  # Установить угол серво 1 в 180 градусов
    servo2.ServoSetAngle(0)  # Установить угол серво 2 в 0 градусов