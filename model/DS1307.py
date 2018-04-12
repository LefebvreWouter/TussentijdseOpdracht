import smbus

class DS1307:
    _ADDRESS_SECONDS = 0x00
    _ADDRESS_MINUTES = 0x01
    _ADDRESS_HOURS = 0x02
    _ADDRESS_DAY = 0x03
    _ADDRESS_DATE = 0x04
    _ADDRESS_MONTH = 0x05
    _ADDRESS_YEAR = 0x06
    _ADDRESS_CONTROL = 0x07

    def __init__(self, i2cbus=1, pAddress=0x68): # 7bits + R/W toevoegen
        self.bus = smbus.SMBus(1) # pi 1 -> bus 0 vanaf pi2 -> bus 2
        self.address = pAddress

    def __BCDtoInt(self, data):
        # 1001 0011

        # 0b(1001) * 10
        #      90
        print(bin(data))
        return ((data >> 4) * 10) + (data & 0x0F)
        # resultaat = 0
        # tupple1 = data >> 4
        # tupple2 = data & 0x0F
        #
        # filter = 0x8
        # for i in range(3, -1, -1):
        #     bit = tupple1 & filter
        #     if bit > 0:
        #        resultaat += pow(2, i) * 10
        #     filter = filter >> 1
        #
        # filter = 0x8
        # for i in range(3, -1, -1):
        #     if (tupple2 & filter) > 0:
        #        resultaat += pow(2, i)
        #     filter = filter >> 1
        # return resultaat

    def __intToBCD(self, data):
        return ((data // 10) << 4) | (data % 10)

    def __read(self, pRegister):
        return self.bus.read_byte_data(self.address, pRegister)

    def __write(self, pRegister, pData):
        return self.bus.write_byte_data(self.address, pRegister, pData)

    # jaren
    def getYear(self):
        return self.__BCDtoInt(self.__read(self._ADDRESS_YEAR))

    def writeYear(self, pJaartal):
        return self.bus.write_byte_data(self.address, self._ADDRESS_YEAR, pJaartal)

    # maanden
    def getMonth(self):
        return self.__BCDtoInt(self.__read(self._ADDRESS_MONTH))

    def writeMonth(self, pMaand):
        return self.bus.write_byte_data(self.address, self._ADDRESS_MONTH, self.__intToBCD(pMaand))

    # dagen
    def getDay(self):
        return self.__BCDtoInt(self.__read(self._ADDRESS_DAY))

    def writeDay(self, pDag):
        return self.bus.write_byte_data(self.address, self._ADDRESS_DAY, self.__intToBCD(pDag))

    # datum
    def getDate(self):
        return self.__BCDtoInt(self.__read(self._ADDRESS_DATE))

    def writeDate(self, pDatum):
        return self.bus.write_byte_data(self.address, self._ADDRESS_DATE, self.__intToBCD(pDatum))

    # uren
    def getHour(self):
        return self.__BCDtoInt(self.__read(self._ADDRESS_HOURS)) + 2

    def writeHour(self, pHour):
        return self.bus.write_byte_data(self.address, self._ADDRESS_HOURS, self.__intToBCD(pHour))

    # minuten
    def getMinute(self):
        return self.__BCDtoInt(self.__read(self._ADDRESS_MINUTES))

    def writeMinute(self, pMinuut):
        return self.bus.write_byte_data(self.address, self._ADDRESS_MINUTES, self.__intToBCD(pMinuut))

    # seconden
    def getSecond(self):
        return self.__BCDtoInt(self.__read(self._ADDRESS_SECONDS))

    def writeSecond(self, pSeconden):
        return self.bus.write_byte_data(self.address, self._ADDRESS_SECONDS, self.__intToBCD(pSeconden))

    # voledige datum
    def getFullDate(self):
        return str(self.getHour()) + ":" + str(self.getMinute()) ###### uur : min
        #return str(self.getHour()) + ":" + str(self.getMinute()) + ":" + str(self.getSecond()) #uur : min : seconden
        #return str(self.getDay()) + "/" + str(self.getMonth()) + "/" + str(self.getYear()) + " " + str(self.getHour()) + ":" + str(self.getMinute()) + ":" + str(self.getSecond()) ## dag : maand: jaar : uur : min : seconden

    def setDateNow(self):
        pass

    def stopClock(self):
        tijdNu = self.getSecond()
        self.bus.write_byte_data(self.address, self._ADDRESS_SECONDS, 128 | tijdNu)
        print('Klok gestopt')