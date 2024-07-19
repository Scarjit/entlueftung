import RPi.GPIO as GPIO


class KY040:

    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    def __init__(self, clockPin, dataPin, switchPin, rotaryCallback=None, switchCallback=None):
        # persist values
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallback = rotaryCallback
        self.switchCallback = switchCallback
        GPIO.setmode(GPIO.BCM)

        #setup pins
        GPIO.setup(clockPin, GPIO.IN)
        GPIO.setup(dataPin, GPIO.IN)
        GPIO.setup(switchPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(clockPin, GPIO.FALLING, callback=self.clkClicked, bouncetime=5)
        GPIO.add_event_detect(dataPin, GPIO.FALLING, callback=self.dtClicked, bouncetime=5)
        GPIO.add_event_detect(switchPin, GPIO.FALLING, callback=self.swClicked, bouncetime=300)

        print("KY040 initialized")

    def clkClicked(self,channel):
        clkState = GPIO.input(self.clockPin)
        dtState = GPIO.input(self.dataPin)
        print("CLK clicked, clkState: ", clkState, " dtState: ", dtState)
        if clkState == 0 and dtState == 1:
            if self.rotaryCallback != None:
                self.rotaryCallback(self.CLOCKWISE)



    def dtClicked(self,channel):
        clkState = GPIO.input(self.clockPin)
        dtState = GPIO.input(self.dataPin)
        print("DT clicked, clkState: ", clkState, " dtState: ", dtState)
        if clkState == 1 and dtState == 0:
            if self.rotaryCallback != None:
                self.rotaryCallback(self.ANTICLOCKWISE)


    def swClicked(self,channel):
        print("SW clicked")
        if self.switchCallback != None:
            self.switchCallback()