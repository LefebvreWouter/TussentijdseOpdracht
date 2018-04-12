from time import sleep
from RPi import GPIO
from TestKlok import TestKlok
from DS1307 import DS1307

class TestSegment:
    def Segment(self):


    Segment()

ds = DS1307()
while True:
    print(ds.getFullDate())
    sleep(1)