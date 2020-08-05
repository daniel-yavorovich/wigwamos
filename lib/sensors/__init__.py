import Adafruit_DHT
import RPi.GPIO as GPIO


class Sensors:
    DHT_PIN = 4
    DHT_SENSOR = Adafruit_DHT.DHT22
    SOIL_MOISTURE_PIN = 21

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SOIL_MOISTURE_PIN, GPIO.IN)

    def get_humidity_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return round(humidity, 2), round(temperature, 2)

    def is_need_watering(self):
        return bool(GPIO.input(self.SOIL_MOISTURE_PIN))
