import Adafruit_DHT


class Sensors:
    DHT_PIN = 4
    DHT_SENSOR = Adafruit_DHT.DHT22

    def __init__(self):
        pass

    def get_sensors_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return round(humidity, 2), round(temperature, 2)
