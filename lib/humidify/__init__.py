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
    HUMIDIFIER_RELAY_NUM = 1
    PUMP_RELAY_NUM = 3

    PUMP_DURATION = 20
    MAX_BOTTLE_CAPACITY = 500

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

    def __is_need_more_water(self):
        return self.__get_total_usage() > self.MAX_BOTTLE_CAPACITY

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
        time.sleep(self.PUMP_DURATION)
        relays.relay_turn_off(self.PUMP_RELAY_NUM)
        logging.debug('Humidifier bottle updated')

    def adjust_humidify(self, relays, current_temperature, current_humidity):
        if not current_temperature or not current_humidity or self.is_disabled():
            return False

        total_usage = self.__get_total_usage()
        logging.debug('Total humidifier usage: {}'.format(total_usage))

        if self.__is_need_more_water():
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
            'is_disabled': self.is_disabled()
        }
