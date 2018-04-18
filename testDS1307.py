from time import sleep
from RPi import GPIO
from DS1307 import DS1307


def testBus():
    import smbus
    # adress = 0x50
    a = 0x53
    # klok
    b = 0x68
    bus = smbus.SMBus(1)
    # data = bus.read_byte_data(b, 0x00)
    bus.write_byte_data(b, 0, 0)

    # print(data)
    # print(bin(data))

testBus()
# sleep(3)

ds = DS1307()

# print(ds.getSecond())

# print(ds.BCDtoInt(0b11011000))
# print(bin(ds.InttoBCD(98)))
while True:
    print(ds.getSecond())

    print(ds.getFullDate())
    sleep(1)
# 1101 0011