import RPi.GPIO as GPIO


class Relays:
    RELAY_PINS = [26, 19, 13, 6]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RELAY_PINS, GPIO.OUT)
        GPIO.output(self.RELAY_PINS, 1)

    def relay_turn_on(self, number):
        GPIO.output(self.RELAY_PINS[number], 0)

    def relay_turn_off(self, number):
        GPIO.output(self.RELAY_PINS[number], 1)
