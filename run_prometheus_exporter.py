import time

from lib.growing import Growing
from lib.sensors import Sensors
from settings import EXPORTER_UPDATE_INTERVAL, EXPORTER_SERVER_PORT
from prometheus_client import start_http_server, Gauge

AIR_TEMPERATURE = Gauge('air_temperature', 'Air temperature')
AIR_HUMIDITY = Gauge('air_humidity', 'Air humidity')
SOIL_MOISTURE = Gauge('soil_moisture', 'Soil moisture')
GROW_DAYS = Gauge('grow_days', 'Grow days')
WATER_LEVEL = Gauge('water_level', 'Water level')
PI_TEMPERATURE = Gauge('pi_temperature', 'Raspberry PI CPU temperature')
LIGHT_BRIGHTNESS = Gauge('light_brightness', 'Light brightness')
FAN_SPEED = Gauge('fan_speed', 'Fan speed')

if __name__ == '__main__':
    sensors = Sensors()
    growing = Growing()
    start_http_server(EXPORTER_SERVER_PORT)

    while True:
        # Get metrics
        humidity, temperature = sensors.get_humidity_temperature()
        soil_moisture = sensors.get_soil_moisture()
        grow_days = growing.get_growing_day_count()

        # Update metrics in exporter
        AIR_HUMIDITY.set(humidity)
        AIR_TEMPERATURE.set(temperature)
        SOIL_MOISTURE.set(soil_moisture)
        GROW_DAYS.set(grow_days)

        time.sleep(EXPORTER_UPDATE_INTERVAL)
