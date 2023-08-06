import serial
from helper import bytes_from_str, crc32_stm, prettify_bytes
from loguru import logger

ser = None

def BCC_Cal(data):
    BCC = 0
    for i in range(len(data)):
        BCC ^= data[i]

    BCC = ~BCC & 0xFF
    return (BCC)


def open(comx, baudrate):
    print("hello world!")
    global ser
    ser = serial.Serial(port=comx, baudrate=baudrate, timeout=1)
    ser.open()


def close():
    global ser
    ser.close()


