import os
import time 
import busio
import board
import sdcardio
import storage

my_file = "my_log.txt"

################################### Настройка
# начальная задержка
time.sleep(1)
# Создание объекта модуля SPI
spi0_module     = busio.SPI(clock=board.IO12, MOSI=board.IO11, MISO=board.IO13)
# Создание объекта для вывода CS
sd_card_cs_pin  = board.IO15

# Создание объекта SDCard
sd_card = sdcardio.SDCard(spi0_module, sd_card_cs_pin)
# Создание объекта файловой системы
vfs     = storage.VfsFat(sd_card)
# Монтирование файловой системы
storage.mount(vfs, '/sd')

################################### Работа

# Открытие файла для записи (режим добавления)
f = open("/sd/"+my_file, "a")
# Запись (следующая строка = "\r\n")
f.write("Hello, world!\r\n")
f.close()

# Размонтирование файловой системы
storage.umount('/sd')