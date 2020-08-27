#!/usr/bin/env python3
import time
import logging

from lib.fan import Fan
from lib.humidify import Humidify
from lib.metrics import Metrics
from lib.properties import Property
from lib.growing import Growing
from lib.light import Light
from lib.relays import Relays
from lib.sensors import Sensors
from lib.triac_hat import TriacHat
from lib.async_helper import run_async
from lib.weather import Weather

from settings import EXPORTER_UPDATE_INTERVAL, EXPORTER_SERVER_PORT, LOG_LEVEL, LIGHT_CONTROL_INTERVAL, \
    FAN_CONTROL_INTERVAL, HUMIDIFY_CONTROL_INTERVAL, UPDATE_WEATHER_INFO_INTERVAL
from prometheus_client import start_http_server as start_prometheus_exporter
from lib.metrics.exporter import *

METRICS = {
    'humidity': 0,
    'temperature': 0,
    'soil_moisture': 1,
}


@run_async
def update_metrics():
    while True:
        # Get properties
        period = growing.get_current_period()
        grow_days = growing.get_growing_day_count()
        light_brightness = light.get_light_brightness()
        fan_speed = fan.get_fan_speed()

        # Get metrics
        water_level = sensors.get_water_level()
        humidity, temperature = sensors.get_humidity_temperature()
        soil_moisture = int(sensors.is_soil_is_wet())
        pi_temperature = sensors.get_pi_temperature()

        # Update local metrics
        if humidity and temperature:
            METRICS['humidity'] = humidity
            METRICS['temperature'] = temperature
        METRICS['soil_moisture'] = soil_moisture

        # Update metrics in exporter
        if humidity and temperature:
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

        target_humidity = humidify.get_target_humidity(temperature)
        if target_humidity:
            TARGET_HUMIDITY.set(target_humidity)

        logging.info('Metrics: H:{humidity}; T:{temperature}; S:{soil_moisture}; W:{water_level}; F:{fan_speed}'.format(
            humidity=humidity,
            temperature=temperature,
            soil_moisture=soil_moisture,
            water_level=water_level,
            fan_speed=fan_speed
        ))

        time.sleep(EXPORTER_UPDATE_INTERVAL)


@run_async
def light_control():
    while True:
        period = growing.get_current_period()
        light.adjust_light(relays, period)
        logging.debug('Light adjusted')
        time.sleep(LIGHT_CONTROL_INTERVAL)


@run_async
def fan_control():
    while True:
        period = growing.get_current_period()
        fan.adjust_fan(triac_hat, period.temperature, metrics.get_avg_temperature('1m'))
        logging.debug('Fan adjusted')
        time.sleep(FAN_CONTROL_INTERVAL)


@run_async
def humidify_control():
    while True:
        humidify.adjust_humidify(relays, metrics.get_avg_temperature('10m'), METRICS['humidity'])
        logging.debug('Humidity adjusted')
        time.sleep(HUMIDIFY_CONTROL_INTERVAL)


@run_async
def update_weather_info():
    while True:
        out_humidity, out_temperature = weather.get_humidity_temperature()

        if out_humidity and out_temperature:
            OUTSIDE_AIR_HUMIDITY.set(out_humidity)
            OUTSIDE_AIR_TEMPERATURE.set(out_temperature)

        time.sleep(UPDATE_WEATHER_INFO_INTERVAL)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=LOG_LEVEL)

    logging.info('Starting...')

    prop = Property()
    relays = Relays()
    triac_hat = TriacHat()
    sensors = Sensors()
    growing = Growing()
    metrics = Metrics()
    fan = Fan()
    light = Light()
    humidify = Humidify()
    weather = Weather()

    # Init start settings
    fan.init(triac_hat)

    start_prometheus_exporter(EXPORTER_SERVER_PORT)
    logging.debug('Prometheus exporter listen on 0.0.0.0:{port}'.format(port=EXPORTER_SERVER_PORT))

    update_metrics()
    light_control()
    fan_control()
    humidify_control()
    update_weather_info()
