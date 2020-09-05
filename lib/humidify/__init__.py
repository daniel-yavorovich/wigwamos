import datetime
import time

import logging

from ..properties import Property
from .vdp import VDP_TEMPERATURE_HUMIDITY
from ..metrics.exporter import HUMIDIFIER_USAGE


class IncorrectTemperature(Exception):
    pass


class Humidify(Property):
    """
    Smart humidity controller
    based on VDP table
    from https://www.alchimiaweb.com/blogen/vapor-pressure-deficit-cannabis-cultivation/
    """
    HUMIDIFY_DISABLED_PROPERTY_NAME = 'humidify_disabled'
    MANUAL_MODE_PROPERTY_KEY = 'humidify_manual_mode'
    MANUAL_HUMIDITY_PROPERTY_KEY = 'humidify_manual_value'
    PUMP_DURATION_PROPERTY_KEY = 'pump_duration'
    PUMP_USAGE_INTERVAL_PROPERTY_KEY = 'pump_usage_interval'

    HUMIDIFIER_RELAY_NUM = 1
    PUMP_RELAY_NUM = 3

    DEFAULT_PUMP_DURATION = 3
    DEFAULT_PUMP_USAGE_INTERVAL = 500

    EXTREME_HUMIDITY_DIFF = 10
    EXTREME_TEMPERATURE_DIFF = 5

    LAST_USAGE = datetime.datetime.now()
    TOTAL_USAGE = 0

    VPD_MIN = 7.6
    MPD_MAX = 10.5

    def __init__(self):
        super().__init__()

    def __update_last_usage(self):
        self.LAST_USAGE = datetime.datetime.now()

    def __get_last_usage(self):
        return self.LAST_USAGE

    def __update_total_usage(self):
        now = datetime.datetime.now()
        usage_seconds = (now - self.__get_last_usage()).seconds

        self.TOTAL_USAGE += usage_seconds
        HUMIDIFIER_USAGE.inc(usage_seconds)

        self.__update_last_usage()

    def __get_total_usage(self):
        return self.TOTAL_USAGE

    def __reset_total_usage(self):
        self.TOTAL_USAGE = 0

    def __is_need_more_water(self, is_humidify_bottle_full):
        if is_humidify_bottle_full:
            logging.debug('Humidify bottle is full')
            return False

        return self.__get_total_usage() > self.pump_usage_interval

    @property
    def pump_usage_interval(self):
        return int(self.get_property_value(self.PUMP_USAGE_INTERVAL_PROPERTY_KEY, self.DEFAULT_PUMP_USAGE_INTERVAL))

    @property
    def pump_duration(self):
        return int(self.get_property_value(self.PUMP_DURATION_PROPERTY_KEY, self.DEFAULT_PUMP_DURATION))

    def set_pump_usage_interval(self, value):
        self.set_property(self.PUMP_USAGE_INTERVAL_PROPERTY_KEY, value)

    def set_pump_duration(self, value):
        self.set_property(self.PUMP_DURATION_PROPERTY_KEY, value)

    def disable(self):
        self.set_property(self.HUMIDIFY_DISABLED_PROPERTY_NAME, 'true')

    def enable(self):
        self.delete_property(self.HUMIDIFY_DISABLED_PROPERTY_NAME)

    def is_disabled(self):
        return bool(self.get_property_value(self.HUMIDIFY_DISABLED_PROPERTY_NAME))

    def set_manual_mode(self, value=False):
        if value:
            self.set_property(self.MANUAL_MODE_PROPERTY_KEY, True)
        else:
            self.delete_property(self.MANUAL_MODE_PROPERTY_KEY)

    def is_manual_mode(self):
        return bool(self.get_property_value(self.MANUAL_MODE_PROPERTY_KEY))

    def make_bottle_full(self, relays):
        relays.relay_turn_on(self.PUMP_RELAY_NUM)
        time.sleep(self.pump_duration)
        relays.relay_turn_off(self.PUMP_RELAY_NUM)
        logging.debug('Humidifier bottle updated')

    def adjust_humidify(self, relays, current_temperature, target_temperature, current_humidity, is_humidify_bottle_full):
        if not current_temperature or not current_humidity or not target_temperature:
            return False

        if self.is_disabled() or self.is_extreme_low_temperature(target_temperature, current_temperature):
            return relays.relay_turn_off(self.HUMIDIFIER_RELAY_NUM)

        total_usage = self.__get_total_usage()
        logging.debug('Total humidifier usage: {}'.format(total_usage))

        if self.__is_need_more_water(is_humidify_bottle_full):
            self.make_bottle_full(relays)
            self.__reset_total_usage()

        target_humidity = self.get_target_humidity(current_temperature)
        if not target_humidity:
            return None

        if current_humidity < target_humidity:
            relays.relay_turn_on(self.HUMIDIFIER_RELAY_NUM)
            self.__update_total_usage()
        else:
            relays.relay_turn_off(self.HUMIDIFIER_RELAY_NUM)

    def get_target_humidity(self, current_temperature):
        if not current_temperature:
            return None

        if self.is_manual_mode():
            value = self.get_manual_humidity()
            if value:
                return value

        try:
            target_humidity_min, target_humidity_max = VDP_TEMPERATURE_HUMIDITY[int(current_temperature)]
            return target_humidity_min
        except KeyError:
            logging.error("Temperature {} is incorrect".format(current_temperature))
            return None

    def set_manual_humidity(self, value):
        self.set_property(self.MANUAL_HUMIDITY_PROPERTY_KEY, str(value))
        self.set_manual_mode(True)

    def get_manual_humidity(self):
        value = self.get_property_value(self.MANUAL_HUMIDITY_PROPERTY_KEY)
        if not value or not self.is_manual_mode():
            return None

        return int(value)

    def get_all_info(self):
        return {
            'manual_humidity': self.get_manual_humidity(),
            'manual_mode': self.is_manual_mode(),
            'is_disabled': self.is_disabled(),
            'pump_usage_interval': self.pump_usage_interval,
            'pump_duration': self.pump_duration,
        }

    def is_extreme_low_humidity(self, target_value, current_value):
        if (target_value - current_value) > self.EXTREME_HUMIDITY_DIFF:
            return True
        return False

    def is_extreme_low_temperature(self, target_value, current_value):
        if (target_value - current_value) > self.EXTREME_TEMPERATURE_DIFF:
            return True
        return False
