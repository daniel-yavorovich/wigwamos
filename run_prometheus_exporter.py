import time
import logging

from lib.fan import Fan
from lib.properties import Property
from lib.growing import Growing
from lib.light import Light
from lib.sensors import Sensors
from settings import EXPORTER_UPDATE_INTERVAL, EXPORTER_SERVER_PORT, LOG_LEVEL
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
    logging.basicConfig(format='%(asctime)s %(message)s', level=LOG_LEVEL)

    prop = Property()
    sensors = Sensors()
    growing = Growing(prop)
    light = Light(prop)
    fan = Fan(prop)

    start_http_server(EXPORTER_SERVER_PORT)

    print('Prometheus exporter listen on 0.0.0.0:{port}'.format(port=EXPORTER_SERVER_PORT))

    while True:
        # Get metrics
        humidity, temperature = sensors.get_humidity_temperature()
        soil_moisture = sensors.get_soil_moisture()
        grow_days = growing.get_growing_day_count()
        water_level = sensors.get_water_level()
        pi_temperature = sensors.get_pi_temperature()
        light_brightness = light.get_light_brightness()
        fan_speed = fan.get_fan_speed()

        # Update metrics in exporter
        AIR_HUMIDITY.set(humidity)
        AIR_TEMPERATURE.set(temperature)
        SOIL_MOISTURE.set(soil_moisture)
        GROW_DAYS.set(grow_days)
        WATER_LEVEL.set(water_level)
        PI_TEMPERATURE.set(pi_temperature)
        LIGHT_BRIGHTNESS.set(light_brightness)
        FAN_SPEED.set(fan_speed)

        time.sleep(EXPORTER_UPDATE_INTERVAL)
