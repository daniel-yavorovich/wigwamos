#!/usr/bin/env python3
import time
import logging
import datetime

from lib.fan import Fan
from lib.properties import Property
from lib.growing import Growing
from lib.light import Light
from lib.relays import Relays
from lib.sensors import Sensors
from settings import EXPORTER_UPDATE_INTERVAL, EXPORTER_SERVER_PORT, LOG_LEVEL, LIGHT_CONTROL_INTERVAL, RUN_INTERVAL
from prometheus_client import start_http_server, Gauge

# Prometheus metrics
AIR_TEMPERATURE = Gauge('air_temperature', 'Air temperature')
AIR_HUMIDITY = Gauge('air_humidity', 'Air humidity')
SOIL_MOISTURE = Gauge('soil_moisture', 'Soil moisture')
GROW_DAYS = Gauge('grow_days', 'Grow days')
WATER_LEVEL = Gauge('water_level', 'Water level')
PI_TEMPERATURE = Gauge('pi_temperature', 'Raspberry PI CPU temperature')
LIGHT_BRIGHTNESS = Gauge('light_brightness', 'Light brightness')
FAN_SPEED = Gauge('fan_speed', 'Fan speed')

# Services
UPDATE_METRICS = 'update_metrics'
LIGHT_CONTROL = 'light_control'
CLIMATE_CONTROL = 'climate_control'
SOIL_MOISTURE_CONTROL = 'soil_moisture_control'

LAST_EXECUTION_TIME = {
    UPDATE_METRICS: None,
    LIGHT_CONTROL: None,
    CLIMATE_CONTROL: None,
    SOIL_MOISTURE_CONTROL: None,
}


def is_need_start(service, interval):
    """
    :param service: service name
    :param interval: seconds count
    :return: True if need start
    """
    now = datetime.datetime.now()

    if not LAST_EXECUTION_TIME[service] or (now - LAST_EXECUTION_TIME[service]).seconds >= interval:
        LAST_EXECUTION_TIME[service] = now
        return True


def update_metrics():
    if not is_need_start(UPDATE_METRICS, EXPORTER_UPDATE_INTERVAL):
        return False

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

    logging.info('Prometheus metrics updated')


def light_control():
    if not is_need_start(LIGHT_CONTROL, LIGHT_CONTROL_INTERVAL):
        return False

    light.adjust_light(period)
    logging.info('Light adjusted')

    # light_brightness = growing.
    # light.set_light_brightness(light_brightness)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=LOG_LEVEL)

    relays = Relays()
    prop = Property()
    sensors = Sensors()
    growing = Growing()
    light = Light(relays)
    fan = Fan()

    start_http_server(EXPORTER_SERVER_PORT)
    logging.info('Prometheus exporter listen on 0.0.0.0:{port}'.format(port=EXPORTER_SERVER_PORT))

    while True:
        period = growing.get_current_period()

        update_metrics()
        light_control()

        time.sleep(RUN_INTERVAL)
