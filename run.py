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
    'temperature': 0
}


@run_async
def update_metrics():
    logging.info('Start update metrics service')
    humidity = None
    temperature = None
    water_level = None
    fan_speed = None

    while True:
        try:
            light_brightness = light.get_light_brightness()
            LIGHT_BRIGHTNESS.set(light_brightness)
        except Exception as e:
            logging.error(e)

        try:
            period = growing.get_current_period()
            grow_days = growing.get_growing_day_count()
            GROW_INFO.info({
                'day': str(grow_days),
                'config': period.config.name,
                'period': period.name,
            })
            TARGET_TEMPERATURE.set(period.temperature)
        except Exception as e:
            logging.error(e)

        try:
            fan_speed = fan.get_fan_speed()
            FAN_SPEED.set(fan_speed)
        except Exception as e:
            logging.error(e)

        if False:
            try:
                water_level = sensors.get_water_level()
                WATER_LEVEL.set(water_level)
            except Exception as e:
                logging.error(e)

        try:
            humidity, temperature = sensors.get_humidity_temperature()
            if humidity and temperature:
                METRICS['humidity'] = humidity
                METRICS['temperature'] = temperature
                AIR_HUMIDITY.set(humidity)
                AIR_TEMPERATURE.set(temperature)

            target_humidity = humidify.get_target_humidity(temperature)
            if target_humidity:
                TARGET_HUMIDITY.set(target_humidity)
        except Exception as e:
            logging.error(e)

        try:
            pi_temperature = sensors.get_pi_temperature()
            PI_TEMPERATURE.set(pi_temperature)
        except Exception as e:
            logging.error(e)

        logging.info('Metrics: H:{humidity}; T:{temperature}; W:{water_level}; F:{fan_speed}'.format(
            humidity=humidity,
            temperature=temperature,
            water_level=water_level,
            fan_speed=fan_speed
        ))

        time.sleep(EXPORTER_UPDATE_INTERVAL)


@run_async
def light_control():
    while True:
        period = growing.get_current_period()
        is_high_temperature = metrics.is_high_temperature()
        light.adjust_light(relays, period, is_high_temperature)
        logging.debug('Light adjusted')
        time.sleep(LIGHT_CONTROL_INTERVAL)


@run_async
def fan_control():
    while True:
        period = growing.get_current_period()
        avg_temperature = metrics.get_avg_temperature('1m')
        target_humidity = humidify.get_target_humidity(avg_temperature)
        is_extreme_low_humidity = humidify.is_extreme_low_humidity(target_humidity, METRICS['humidity'])

        if period.fan == -1:
            fan.adjust_fan(triac_hat, period.temperature, avg_temperature, is_extreme_low_humidity)
        else:
            fan.set_fan_speed(triac_hat, period.fan)

        logging.debug('Fan adjusted')
        time.sleep(FAN_CONTROL_INTERVAL)


@run_async
def humidify_control():
    while True:
        period = growing.get_current_period()

        if not period.humidity:
            return None
        elif period.humidity == -1:
            target_humidity = None
        else:
            target_humidity = period.humidity

        humidify.adjust_humidify(relays, metrics.get_avg_temperature('10m'), period.temperature,
                                 METRICS['humidity'],
                                 sensors.is_humidify_bottle_full(), target_humidity)

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
