import time
import board
import busio
from lib import LSM6DSL

################################### Настройка
# начальная задержка
time.sleep(1)
# Создаем объект модуля i2c
i2c1_module = busio.I2C(scl=board.IO2, sda=board.IO3)
# Создаем объект lsm6dsl
lsm6dsl     = LSM6DSL.LSM6DSL_I2C(i2c1_module, LSM6DSL.LSM6DSL_DEFAULT_ADDRESS)

################################### Работа
while True:
    # Получаем данные с устройства
    acc = lsm6dsl.acceleration()
    gyro = lsm6dsl.gyro()
    temp = lsm6dsl.temperature()
    
    # выводим
    print(f"\nТемпература   : {temp} C")
    print(f"Ускорение: X:{acc[0]}, Y: {acc[1]}, Z: {acc[2]} м/с^2")
    print(f"Гироскоп: X:{gyro[0]}, Y: {gyro[1]}, Z: {gyro[2]} градусов/с")
    time.sleep(0.5)