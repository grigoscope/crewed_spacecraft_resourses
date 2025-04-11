import time
import board
import busio
import sys

from lib import GNSS

# Задержка перед началом работы
time.sleep(1)

# Инициализация UART для работы с GNSS модулем
gnss_uart = busio.UART(board.IO17, board.IO18, baudrate=9600, timeout=10)

# Создание объекта GNSS
gnss = GNSS.GPS(gnss_uart, debug=False)

# Отправка команды для настройки вывода данных GNSS
gnss.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Установка частоты обновления данных GNSS (1000 мс = 1 секунда)
gnss.send_command(b"PMTK220,1000")

# Основной цикл программы
while True:
    # Обновление данных GNSS
    gnss.update()

    # Вывод широты и долготы
    print(f"Широта: {gnss.latitude} Долгота: {gnss.longitude}")