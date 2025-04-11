import board
import time

from lib import DC_MOTOR

################################### Настройка

# МОТОР A
xIN1_PWM_pin  = board.IO21
xIN2_GPIO_pin = board.IO47

# МОТОР B - общий с сервоприводами 3/4
# xIN1_PWM_pin  = board.IO42
# xIN2_GPIO_pin = board.IO41

dc_mot = DC_MOTOR.MOTOR(xIN1_PWM_pin, xIN2_GPIO_pin)

################################### Работа
# Начальная точка
speed = 0
dir   = 1
while True:
    time.sleep(0.05)
    # Изменение направления
    if(dir == 1  and speed == 100):
        dir = -1
    if(dir == -1 and speed == -100):
        dir = 1

    # Изменение скорости
    speed += dir
    dc_mot.DCMotorSetSpeed(speed)

    # Вывод
    print(f"Direction : {dir}, Speed: {speed}")