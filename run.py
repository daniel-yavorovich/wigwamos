#!/usr/bin/env python3
import time
import logging
import datetime

from lib.fan import Fan
from lib.humidify import Humidify
from lib.metrics import Metrics
from lib.properties import Property
from lib.growing import Growing
from lib.light import Light
from lib.relays import Relays
from lib.sensors import Sensors
from lib.triac_hat import TriacHat
from lib.watering import Watering
from lib.async_helper import run_async
from settings import EXPORTER_UPDATE_INTERVAL, EXPORTER_SERVER_PORT, LOG_LEVEL, LIGHT_CONTROL_INTERVAL, \
    FAN_CONTROL_INTERVAL, RUN_INTERVAL, SOIL_MOISTURE_CONTROL_INTERVAL, HUMIDIFY_CONTROL_INTERVAL
from prometheus_client import start_http_server, Gauge, Info

# Prometheus metrics
GROW_INFO = Info('growing', 'Grow info')
AIR_TEMPERATURE = Gauge('air_temperature', 'Air temperature')
AIR_HUMIDITY = Gauge('air_humidity', 'Air humidity')
SOIL_MOISTURE = Gauge('soil_moisture', 'Soil moisture')
WATER_LEVEL = Gauge('water_level', 'Water level')
PI_TEMPERATURE = Gauge('pi_temperature', 'Raspberry PI CPU temperature')
LIGHT_BRIGHTNESS = Gauge('light_brightness', 'Light brightness')
FAN_SPEED = Gauge('fan_speed', 'Fan speed')
TARGET_TEMPERATURE = Gauge('target_temperature', 'Target temperature')
TARGET_HUMIDITY = Gauge('target_humidity', 'Target humidity')

# Services
UPDATE_METRICS = 'update_metrics'
LIGHT_CONTROL = 'light_control'
FAN_CONTROL = 'fan_control'
HUMIDIFY_CONTROL = 'humidify_control'
SOIL_MOISTURE_CONTROL = 'soil_moisture_control'

LAST_EXECUTION_TIME = {
    UPDATE_METRICS: None,
    LIGHT_CONTROL: None,
    FAN_CONTROL: None,
    HUMIDIFY_CONTROL: None,
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


@run_async
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
    GROW_INFO.info({
        'day': str(grow_days),
        'config': period.config.name,
        'period': period.name,
    })
    WATER_LEVEL.set(water_level)
    PI_TEMPERATURE.set(pi_temperature)
    LIGHT_BRIGHTNESS.set(light_brightness)
    FAN_SPEED.set(fan_speed)
    TARGET_TEMPERATURE.set(period.temperature)
    TARGET_HUMIDITY.set(period.humidity)

    logging.info('Prometheus metrics updated')


@run_async
def light_control():
    if not is_need_start(LIGHT_CONTROL, LIGHT_CONTROL_INTERVAL):
        return False

    light.adjust_light(period)
    logging.info('Light adjusted')


@run_async
def fan_control():
    if not is_need_start(FAN_CONTROL, FAN_CONTROL_INTERVAL):
        return False

    temperature = metrics.get_avg_temperature()
    fan.adjust_fan(period, temperature)
    logging.info('Fan adjusted')


@run_async
def watering_control():
    if not is_need_start(SOIL_MOISTURE_CONTROL, SOIL_MOISTURE_CONTROL_INTERVAL):
        return False

    avg_soil_moisture = metrics.get_avg_soil_moisture()
    watering.adjust_watering(avg_soil_moisture)
    logging.info('Soil moisture adjusted')


@run_async
def humidify_control():
    if not is_need_start(HUMIDIFY_CONTROL, HUMIDIFY_CONTROL_INTERVAL):
        return False

    avg_humidity = metrics.get_avg_humidity()
    humidify.adjust_humidify(period, avg_humidity)
    logging.info('Humidity adjusted')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=LOG_LEVEL)

    logging.info('Waiting 30 sec before start for loading Triac HAT module...')
    # time.sleep(30)
    logging.info('Starting...')

    prop = Property()
    relays = Relays()
    triac_hat = TriacHat()
    sensors = Sensors()
    growing = Growing()
    metrics = Metrics()
    light = Light(relays)
    fan = Fan(triac_hat)
    watering = Watering(relays)
    humidify = Humidify(relays)

    start_http_server(EXPORTER_SERVER_PORT)
    logging.info('Prometheus exporter listen on 0.0.0.0:{port}'.format(port=EXPORTER_SERVER_PORT))

    while True:
        period = growing.get_current_period()

        t1 = update_metrics()
        t2 = light_control()
        t3 = fan_control()
        t4 = watering_control()
        t5 = humidify_control()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

        time.sleep(RUN_INTERVAL)
