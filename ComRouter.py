import serial
import Queue
from threading import Thread

class Com1(Thread):

    def __init__(self):
        ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200,
                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)



class Com2(Thread):

    def __init__(self):
        ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200,
                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)


class MessageQ(Thread):
    def __init__(self):
        pass


