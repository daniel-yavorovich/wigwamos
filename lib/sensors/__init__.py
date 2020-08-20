import os
import re
import Adafruit_DHT
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
from settings import BOTTLE_HEIGHT


class Sensors:
    DHT_SENSOR = Adafruit_DHT.DHT22

    DHT_PIN = 4
    SOIL_MOISTURE_PIN = 21
    RANGING_MODULE_TRIGGER_PIN = 22
    RANGING_MODULE_ECHO_PIN = 27

    def __init__(self):
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SOIL_MOISTURE_PIN, GPIO.IN)

        self.distance_sensor = DistanceSensor(trigger=self.RANGING_MODULE_TRIGGER_PIN,
                                              echo=self.RANGING_MODULE_ECHO_PIN)

    def get_humidity_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        if not humidity or not humidity:
            return None, None

        return round(humidity, 2), round(temperature, 2)

    def get_soil_moisture(self):
        """
        0: all is well
        1: need watering!
        """
        return int(GPIO.input(self.SOIL_MOISTURE_PIN))

    def get_water_level(self):
        """
        Returns the percentage
        of full water bottle
        """

        distance_to_water = self.distance_sensor.distance * 100

        if distance_to_water > 1000:
            distance_to_water = 0

        result = 100 - (distance_to_water - 1 / BOTTLE_HEIGHT * 100)

        if result < 0:
            result = 0

        if result > 100:
            result = 100

        return round(result, 2)

    def get_pi_temperature(self):
        temp = os.popen("vcgencmd measure_temp").readline()
        return float(re.search(r'temp=(\d+\.\d+)\'C\n', temp).group(1))
