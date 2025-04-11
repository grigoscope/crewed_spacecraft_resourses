import board
import time 

from lib import GPIO_MUX

################################### Настройка
# Создаем объект мультиплексора с указанием пинов для управления и ввода/вывода
mux = GPIO_MUX.MUX(s0=board.IO46, s1=board.IO0, s2=board.IO39, inout=board.IO1)
# Выбираем линию мультиплексора (номер 4)
mux.muxSelectLine(4)

################################### Работа
while True:
    # Переключаем мультиплексор в режим аналогового ввода
    mux.mux2Analog()
    # Считываем значение с пина ввода/вывода
    photoresistor_raw = mux.mux_inout.value
    # Выводим значение с датчика на экран
    print(f"Значение на светодатчике: {photoresistor_raw}")