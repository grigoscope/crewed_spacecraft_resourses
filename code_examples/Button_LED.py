import board
import digitalio

################################### Настройка
#Создаем объект кнопки
button           = digitalio.DigitalInOut(board.IO9)
button.direction = digitalio.Direction.INPUT
button.pull      = digitalio.Pull.UP

#Создаем объект светодиода
led = digitalio.DigitalInOut(board.IO8)
led.direction = digitalio.Direction.OUTPUT

################################### Работа
while True:
    #светодиод != кнопка
    led.value = not button.value