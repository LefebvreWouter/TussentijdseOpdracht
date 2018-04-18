import RPi.GPIO as GPIO
import time
from threading import Thread

segment1 = 21
segment2 = 20
segment3 = 16
segment4 = 12

# SHIFT REGISTER
DS = 26
ST_CP = 13
SH_CP = 6

segments = [21, 20, 16, 12]

# dictionary met de verschillende getallen, en welke waarden er hoog of laag moeten voor staan
num = {'0': [1, 1, 0, 0, 0, 0, 0, 0],
       '1': [1, 1, 1, 1, 1, 0, 0, 1],
       '2': [1, 0, 1, 0, 0, 1, 0, 0],
       '3': [1, 0, 1, 1, 0, 0, 0, 0],
       '4': [1, 0, 0, 1, 1, 0, 0, 1],
       '5': [1, 0, 0, 1, 0, 0, 1, 0],
       '6': [1, 0, 0, 0, 0, 0, 1, 0],
       '7': [1, 1, 1, 0, 1, 1, 0, 0],
       '8': [1, 0, 0, 0, 0, 0, 0, 0],
       '9': [1, 0, 0, 1, 0, 0, 0, 0]}

# dictionary voor de getallen als er een punt (.) in zit
num_met_punt = {'0': [0, 1, 0, 0, 0, 0, 0, 0],
               '1': [0, 1, 1, 1, 1, 0, 0, 1],
               '2': [0, 0, 1, 0, 0, 1, 0, 0],
               '3': [0, 0, 1, 1, 0, 0, 0, 0],
               '4': [0, 0, 0, 1, 1, 0, 0, 1],
               '5': [0, 0, 0, 1, 0, 0, 1, 0],
               '6': [0, 0, 0, 0, 0, 0, 1, 0],
               '7': [0, 1, 1, 0, 1, 1, 0, 0],
               '8': [0, 0, 0, 0, 0, 0, 0, 0],
               '9': [0, 0, 0, 1, 0, 0, 0, 0]}



class SegmentDisplay:

    threadrun = False

    def __init__(self):

        #Geen melding krijgen van gereserveerde pinnen
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DS, GPIO.OUT)
        GPIO.setup(ST_CP, GPIO.OUT)
        GPIO.setup(SH_CP, GPIO.OUT)

        #elk segment als een output weergeven en daarbij ook meteen het segment afleggen
        for segment in segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 1)


    def initShiftRegister(self):
        GPIO.output(SH_CP, GPIO.HIGH)
        GPIO.output(SH_CP, GPIO.LOW)

    def copyToStorageRegister(self):
        GPIO.output(ST_CP, GPIO.HIGH)
        #time.sleep(0.005)
        GPIO.output(ST_CP, GPIO.LOW)
        # functie die waardes doorstuurd naar het shift register, het shift register zorgt ervoor dat het gewenste getal op het 7 segment display komt

    def digit(self,digit, puntjeAan):

        if (puntjeAan):
            for getal, value in num_met_punt.items():
                if getal == digit:
                    values = value
                    for a in values:
                        GPIO.output(DS, a)
                        self.initShiftRegister()
                        self.copyToStorageRegister()
        else:
            for getal, value in num.items():
                if getal == digit:
                    values = value
                    for a in values:
                        GPIO.output(DS, a)
                        self.initShiftRegister()
                        self.copyToStorageRegister()


    def met_punt(self,getal):
        gesplitst_getal = ""

        for waarde in getal:
            gesplitst_getal += waarde + ";"

        list_getal = list(gesplitst_getal)
        positie = list_getal.index(".")
        list_getal.insert((positie - 1), ".")
        del (list_getal[positie + 1])
        del (list_getal[positie + 1])
        list_getal.pop()
        str_getal = ""
        for waarde in list_getal:
            str_getal += waarde
        getal_info = str_getal.split(";")
        return getal_info

        # correct splitsen voor gehele getallen

    def zonder_punt(self,getal):
        gesplitst_getal = ""

        for waarde in getal:
            gesplitst_getal += waarde + ";"

        list_getal = list(gesplitst_getal)
        list_getal.pop()

        str_getal = ""
        for waarde in list_getal:
            str_getal += waarde
        getal_info = str_getal.split(";")
        return getal_info

        # kijken of het getal met een punt is of zonder punt

    def splitsing(self,getal):
        if getal.find(".") > -1:
            print("JA")
            return num_met_punt(getal)
        else:
            print("Nee")
            return num(getal)


            # lengte bepalen en positie bepalen van de cijfers, om +- 5 seconden wordt een nieuwe waarde ingegeven

    def uitvoeren(self,timeArray):
        self.threadrun = True;
        thread = Thread(target=self.background_task, args=[timeArray])
        thread.start()

    def setThreadRun(self, threadvalue):
        self.threadrun = threadvalue

    def background_task(self, timeArray):
        GPIO.output(segment1, 0)
        GPIO.output(segment2, 0)
        GPIO.output(segment3, 0)
        GPIO.output(segment4, 0)

        while self.threadrun:
            self.digit(timeArray[0], False)
            GPIO.output(segment1, 1)
            time.sleep(0.001)
            GPIO.output(segment1, 0)

            self.digit(timeArray[1], True)
            GPIO.output(segment2, 1)
            time.sleep(0.001)
            GPIO.output(segment2, 0)

            self.digit(timeArray[2], False)
            GPIO.output(segment3, 1)
            time.sleep(0.001)
            GPIO.output(segment3, 0)

            self.digit(timeArray[3], False)
            GPIO.output(segment4, 1)
            time.sleep(0.001)
            GPIO.output(segment4, 0)
