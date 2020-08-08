from prometheus_client import start_http_server, Gauge
import time

from lib.sensors import Sensors

EXPORTER_SERVER_PORT = 8000
RUN_INTERVAL = 10

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

    start_http_server(EXPORTER_SERVER_PORT)
    while True:
        # Get metrics
        humidity, temperature = sensors.get_humidity_temperature()

        # Update metrics in exporter
        AIR_HUMIDITY.set(humidity)
        AIR_TEMPERATURE.set(temperature)

        time.sleep(RUN_INTERVAL)
