import time
import board
import adafruit_hcsr04

trigger_pin=board.IO21 # Пин A02, используется для отправки ультразвукового сигнала
echo_pin=board.IO14    # Пин A03, используется для приема отраженного ультразвукового сигнала

# Создаем объект для работы с ультразвуковым датчиком HC-SR04
sonar = adafruit_hcsr04.HCSR04(trigger_pin=trigger_pin, echo_pin=echo_pin)

# Бесконечный цикл для измерения расстояния
while True:
        print((sonar.distance,))
        # Задержка в 0.1 секунды перед следующим измерением
        time.sleep(0.1)