import serial
import webpy

def BCC_Cal(data):
    BCC = 0
    for i in range(len(data)):
        BCC ^= data[i]

    BCC = ~BCC & 0xFF
    return (BCC)

def init():
    print("hello world!")
