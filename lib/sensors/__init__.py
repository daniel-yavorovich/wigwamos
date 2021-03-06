import logging
import Adafruit_DHT
from settings import BOTTLE_HEIGHT
from gpiozero import DistanceSensor, Button, CPUTemperature


class Sensors:
    DHT_SENSOR = Adafruit_DHT.DHT22

    DHT_PIN = 5
    HUMIDIFY_WATER_LEVEL_PIN = 21
    RANGING_MODULE_TRIGGER_PIN = 22
    RANGING_MODULE_ECHO_PIN = 27

    def __init__(self):
        self.humidify_water_level_sensor = Button(self.HUMIDIFY_WATER_LEVEL_PIN)
        self.distance_sensor = DistanceSensor(trigger=self.RANGING_MODULE_TRIGGER_PIN,
                                              echo=self.RANGING_MODULE_ECHO_PIN)
        self.cpu_temperature_sensor = CPUTemperature()

    def get_humidity_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        if not humidity or not temperature or humidity > 100:
            return None, None

        return round(humidity, 2), round(temperature, 2)

    def is_humidify_bottle_full(self):
        return not self.humidify_water_level_sensor.is_active

    def get_water_level(self):
        """
        Returns the percentage
        of full water bottle
        """

        try:
            distance_to_water = self.distance_sensor.distance * 100
        except Exception as e:
            logging.warning(e)
            distance_to_water = 0

        if distance_to_water > 1000:
            distance_to_water = 0

        result = 100 - ((distance_to_water - 1) / BOTTLE_HEIGHT * 100)

        if result < 0:
            result = 0

        if result > 100:
            result = 100

        return round(result, 2)

    def get_pi_temperature(self):
        return round(self.cpu_temperature_sensor.temperature, 2)
