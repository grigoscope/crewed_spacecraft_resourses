import time
import board
import mpu6050
import busio

# Инициализация интерфейса I2C с использованием указанных пинов
i2c = busio.I2C(scl=board.IO2, sda=board.IO3)  # использует board.SCL и board.SDA
# Инициализация датчика MPU6050
mpu = mpu6050.MPU6050(i2c)

# Бесконечный цикл для считывания данных с датчика
while True:
    # Вывод данных об ускорении по осям X, Y, Z
    print("Ускорение: X:%.2f, Y: %.2f, Z: %.2f м/с^2" % (mpu.acceleration))
    # Вывод данных о гироскопе по осям X, Y, Z
    print("Гироскоп: X:%.2f, Y: %.2f, Z: %.2f рад/с" % (mpu.gyro))
    # Вывод температуры
    print("Температура: %.2f C" % mpu.temperature)
    print("")
    # Задержка перед следующим измерением
    time.sleep(0.1)