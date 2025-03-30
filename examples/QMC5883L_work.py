import time
import board
import busio
import math
from lib import QMC5883L

################################### Настройка
# начальная задержка
time.sleep(1)
# Создаем объект модуля i2c
i2c1_module = busio.I2C(scl=board.IO2, sda=board.IO3)
# Создаем объект qmc5883l
qmc5883l     = QMC5883L.QMC5883L_I2C(i2c1_module, QMC5883L.QMC5883L_DEFAULT_ADDRESS)

################################### Работа
while True:
    # Получаем данные с устройства
    temp = qmc5883l.temperature()
    mag = qmc5883l.magnetometer()

    # выводим
    print(f"\nТемпература   : {temp} C") # Относительная!
    print(f"Магнитометр: X:{mag[0]}, Y: {mag[1]}, Z: {mag[2]} мТл")

    time.sleep(0.5)