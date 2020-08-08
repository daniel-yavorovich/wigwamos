import time

import Adafruit_DHT
import RPi.GPIO as GPIO


class Sensors:
    DHT_SENSOR = Adafruit_DHT.DHT22

    DHT_PIN = 4
    SOIL_MOISTURE_PIN = 21
    RANGING_MODULE_TRIGGER_PIN = 22
    RANGING_MODULE_ECHO_PIN = 27

    BOTTLE_HEIGHT = 23.6

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SOIL_MOISTURE_PIN, GPIO.IN)

        GPIO.setup(self.RANGING_MODULE_TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.RANGING_MODULE_ECHO_PIN, GPIO.IN)

    def get_humidity_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return round(humidity, 2), round(temperature, 2)

    def is_need_watering(self):
        return bool(GPIO.input(self.SOIL_MOISTURE_PIN))

    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.RANGING_MODULE_TRIGGER_PIN, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.RANGING_MODULE_TRIGGER_PIN, False)

        start_time = time.time()
        stop_time = time.time()

        # save StartTime
        while GPIO.input(self.RANGING_MODULE_ECHO_PIN) == 0:
            start_time = time.time()

        # save time of arrival
        while GPIO.input(self.RANGING_MODULE_ECHO_PIN) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        time_elapsed = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (time_elapsed * 34300) / 2

        return distance

    def get_water_level(self):
        """
        Returns the percentage
        of full water bottle
        """
        distance_to_water = self.get_distance()
        if distance_to_water > 1000:
            distance_to_water = 0

        result = 100 - (distance_to_water / self.BOTTLE_HEIGHT * 100)

        return round(result, 2)
