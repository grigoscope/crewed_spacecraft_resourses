import pwmio
import board
import time

frequency_buzzer = 1000 # В Гц

################################### Настройка
# Создаем объект для пина зуммера
buzzer_pin = board.IO4
# Создаем объект зуммера
buzzer = pwmio.PWMOut(pin=buzzer_pin, duty_cycle=0, frequency=frequency_buzzer, variable_frequency=True)

# Включить зуммер
def BuzzerOn(frequency):
    buzzer.frequency = frequency
    buzzer.duty_cycle = 32768
# Выключить зуммер
def BuzzerOff():
    buzzer.duty_cycle = 0

################################### Работа
while True:
    time.sleep(0.3)
    BuzzerOn(1000)
    time.sleep(0.3)
    BuzzerOff()