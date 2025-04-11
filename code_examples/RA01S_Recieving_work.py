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

# Создание объектов пинов
Ra01S_cs_pin    = board.IO7
Ra01S_nRst_pin  = board.IO6
Ra01S_nInt_pin  = board.IO5

# Создание объекта Ra01S
Ra01S     = Ra01S.Ra01S_SPI(spi0_module, Ra01S_cs_pin, Ra01S_nRst_pin, Ra01S_nInt_pin, spi0_speed)

# Первая инициализация и включение
Ra01S.on()

# Установка режима энергосбережения
Ra01S.SetLowPower()
#Ra01S.SetLowPower()

# Выбор канала 0-6
Ra01S.SetChannel(6) 

main_uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

################################### Работа
num_string_msg = 0
# Основной цикл программы
while True:
    print(f"{Ra01S.ReciveS()}", end="")