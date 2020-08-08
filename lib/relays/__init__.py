import RPi.GPIO as GPIO


class RelayNumberTooLarge(Exception):
    pass


class Relays:
    RELAY_PINS = [26, 19, 13, 6]

    def __init__(self):
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RELAY_PINS, GPIO.OUT)
        GPIO.output(self.RELAY_PINS, 1)

    @staticmethod
    def __validate_relay_num(num):
        if num > 3:
            raise RelayNumberTooLarge("Available only 4 relays: from 0 to 3")

    def relay_turn_on(self, number):
        self.__validate_relay_num(number)
        GPIO.output(self.RELAY_PINS[number], 0)

    def relay_turn_off(self, number):
        self.__validate_relay_num(number)
        GPIO.output(self.RELAY_PINS[number], 1)
