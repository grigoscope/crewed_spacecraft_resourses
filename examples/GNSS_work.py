import time
import board
import busio
import sys

from lib import GNSS

time.sleep(1)

gnss_uart = busio.UART(board.IO17, board.IO18, baudrate=9600, timeout=10)

gnss = GNSS.GPS(gnss_uart, debug=False)


gnss.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gnss.send_command(b"PMTK220,1000")


while True:

    gnss.update()

    print("Latitude: {0:.6f} degrees".format(gnss.latitude))
    print("Longitude: {0:.6f} degrees".format(gnss.longitude))
