from DS1307 import DS1307
from SegmentDisplay import SegmentDisplay
import time




class main:

    previousTime = 0
    ds = DS1307()
    segmentDisplay = SegmentDisplay()

    def __init__(self):
        timeArray = self.ds.getTime()
        self.previousTime = timeArray[3]
        self.segmentDisplay.uitvoeren(timeArray)

        while True:
            self.run()
            time.sleep(5)


    def run(self):
        timeArray = self.ds.getTime()
        timeChanged = self.checkTime(timeArray)

        if (timeChanged):
            self.segmentDisplay.setThreadRun(False)
            time.sleep(0.05)
            self.segmentDisplay.uitvoeren(timeArray)

    def checkTime(self, timeArray ):
        if (self.previousTime != timeArray[3]):
            self.previousTime = timeArray[3]
            return True
        else:
            return False


main()