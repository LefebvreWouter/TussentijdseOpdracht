from DS1307 import DS1307


import RPi.GPIO as GPIO
import time




def main():
    #declaratie van de verschillende segmenten, lijsten waar de waardes inkomen van de temperatuur en lichtpercentage, de klokken van  het shift register, de verschillende cijfers in een lijst
    #4x7 Segment Display
    segment1 = 21
    segment2 = 20
    segment3 = 16
    segment4 = 12


    #SHIFT REGISTER
    DS = 26
    ST_CP = 13
    SH_CP = 6

    segments = [21, 20, 16, 12]


    #Geen melding krijgen van gereserveerde pinnen
    GPIO.setwarnings(False)


    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DS, GPIO.OUT)
        GPIO.setup(ST_CP, GPIO.OUT)
        GPIO.setup(SH_CP, GPIO.OUT)

    def initShiftRegister():
        GPIO.output(SH_CP, GPIO.HIGH)
        GPIO.output(SH_CP, GPIO.LOW)

    def copyToStorageRegister():
        GPIO.output(ST_CP, GPIO.HIGH)
        time.sleep(0.005)
        GPIO.output(ST_CP, GPIO.LOW)

    init()

    #elk segment als een output weergeven en daarbij ook meteen het segment afleggen
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 1)

    #dictionary met de verschillende getallen, en welke waarden er hoog of laag moeten voor staan
    num = {'0': [0, 0, 1, 1, 1, 1, 1, 1],
           '1': [0, 0, 0, 0, 0, 1, 1, 0],
           '2': [0, 1, 0, 1, 1, 0, 1, 1],
           '3': [0, 1, 0, 0, 1, 1, 1, 1],
           '4': [0, 1, 1, 0, 0, 1, 1, 0],
           '5': [0, 1, 1, 0, 1, 1, 0, 1],
           '6': [0, 1, 1, 1, 1, 1, 0, 1],
           '7': [0, 0, 0, 0, 0, 1, 1, 1],
           '8': [0, 1, 1, 1, 1, 1, 1, 1],
           '9': [0, 1, 1, 0, 1, 1, 1, 1]}

    #dictionary voor de getallen als er een punt (.) in zit
    num_met_punt = {'0': [1, 0, 1, 1, 1, 1, 1, 1],
                    '1': [1, 0, 0, 0, 0, 1, 1, 0],
                    '2': [1, 1, 0, 1, 1, 0, 1, 1],
                    '3': [1, 1, 0, 0, 1, 1, 1, 1],
                    '4': [1, 1, 1, 0, 0, 1, 1, 0],
                    '5': [1, 1, 1, 0, 1, 1, 0, 1],
                    '6': [1, 1, 1, 1, 1, 1, 0, 1],
                    '7': [1, 0, 0, 0, 0, 1, 1, 1],
                    '8': [1, 1, 1, 1, 1, 1, 1, 1],
                    '9': [1, 1, 1, 0, 1, 1, 1, 1]}

    #functie die waardes doorstuurd naar het shift register, het shift register zorgt ervoor dat het gewenste getal op het 7 segment display komt
    def digit(digit):
        i = 0

        if len(digit) == 1:
            for getal, value in num.items():
                if getal == digit:
                    values = value
                    for a in values:
                        GPIO.output(DS, a)
                        initShiftRegister()
                        i += 1

                    copyToStorageRegister()

        else:
            gesplitsde_digit = digit[0]
            for getal, value in num_met_punt.items():
                if getal == gesplitsde_digit:
                    values = value
                    for a in values:
                        GPIO.output(DS, a)
                        initShiftRegister()
                        i += 1

                    copyToStorageRegister()
                    # print(values)

    #correct splitsen voor de kommagetallen
    def met_punt(getal):
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

    #correct splitsen voor gehele getallen
    def zonder_punt(getal):
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

    #kijken of het getal met een punt is of zonder punt
    def splitsing(getal):
        if getal.find(".") > -1:
            print("JA")
            return met_punt(getal)
        else:
            print("Nee")
            return zonder_punt(getal)


    #lengte bepalen en positie bepalen van de cijfers, om +- 5 seconden wordt een nieuwe waarde ingegeven
    def uitvoeren(functie_splitsing):
        lengte = len(functie_splitsing)
        run = True
        i = 0

        if lengte == 1:
            while run == True:
                GPIO.output(segment1, 1)
                GPIO.output(segment2, 1)
                GPIO.output(segment3, 1)

                GPIO.output(segment4, 0)
                digit(functie_splitsing[-1])
                GPIO.output(segment4, 1)


                i += 1



        elif lengte == 2:
            while run == True:
                GPIO.output(segment1, 1)
                GPIO.output(segment2, 1)

                GPIO.output(segment3, 0)
                digit(functie_splitsing[-2])
                GPIO.output(segment3, 1)

                GPIO.output(segment4, 0)
                digit(functie_splitsing[-1])
                GPIO.output(segment4, 1)


                i += 1


        elif lengte == 3:
            while run == True:
                GPIO.output(segment1, 1)

                GPIO.output(segment2, 0)
                digit(functie_splitsing[-3])
                GPIO.output(segment2, 1)

                GPIO.output(segment3, 0)
                digit(functie_splitsing[-2])
                GPIO.output(segment3, 1)

                GPIO.output(segment4, 0)
                digit(functie_splitsing[-1])
                GPIO.output(segment4, 1)


                i += 1



        elif lengte == 4:
            while run == True:
                GPIO.output(segment1, 0)
                digit(functie_splitsing[-4])
                GPIO.output(segment1, 1)

                GPIO.output(segment2, 0)
                digit(functie_splitsing[-3])
                GPIO.output(segment2, 1)

                GPIO.output(segment3, 0)
                digit(functie_splitsing[-2])
                GPIO.output(segment3, 1)

                GPIO.output(segment4, 0)
                digit(functie_splitsing[-1])
                GPIO.output(segment4, 1)


                i += 1



        else:
            print("Foutieve invoer!")


main()
