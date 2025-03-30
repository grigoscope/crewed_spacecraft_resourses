import time
import board
import digitalio
import busio
import math
from lib import Ra01S

################################### Настройка
# начальная задержка
time.sleep(1)

# Создание объекта SDCard_cs_pin
SDCard_cs_pin  = board.IO15

# Создание объекта SDCard_cs, (!) перед инициализацией SPI
SDCard_cs = digitalio.DigitalInOut(SDCard_cs_pin)
SDCard_cs.direction = digitalio.Direction.OUTPUT
SDCard_cs.value = True

# Создание объекта модуля SPI
spi0_speed = 2000000
spi0_module     = busio.SPI(clock=board.IO12, MOSI=board.IO11, MISO=board.IO13)

# Создание объектов для пинов
Ra01S_cs_pin    = board.IO7
Ra01S_nRst_pin  = board.IO6
Ra01S_nInt_pin  = board.IO5

# Создание объекта Ra01S_cs
Ra01S_cs = digitalio.DigitalInOut(Ra01S_cs_pin)
Ra01S_cs.direction = digitalio.Direction.OUTPUT
Ra01S_cs.value = True

# Создание объекта Ra01S_nRst
Ra01S_nRst = digitalio.DigitalInOut(Ra01S_nRst_pin)
Ra01S_nRst.direction = digitalio.Direction.OUTPUT
Ra01S_nRst.value = True

# Создание объекта Ra01S_nInt
Ra01S_nInt = digitalio.DigitalInOut(Ra01S_nInt_pin)
Ra01S_nInt.direction = digitalio.Direction.INPUT

# Создание объекта Ra01S
Ra01S     = Ra01S.Ra01S_SPI(spi0_module, Ra01S_cs, Ra01S_nRst, Ra01S_nInt, spi0_speed)

# Первая инициализация и включение
Ra01S.on()

# Установка режима низкого энергопотребления
Ra01S.SetLowPower()
# Ra01S.SetLowPower()

# Выбор канала 0-6
Ra01S.SetChannel(0) 

################################### Работа
while True:
    # Отправка строки "Hello!\n"
    Ra01S.SendS("Hello!\n")
    print("Отправлено сообщение: Hello")
    
    # Задержка 0.5 секунды
    time.sleep(0.5)