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
    HUMIDIFIER_RELAY_NUM = 1
    PUMP_RELAY_NUM = 3

    PUMP_DURATION = 15
    MAX_BOTTLE_CAPACITY = 300

    LAST_USAGE = datetime.datetime.now()
    TOTAL_USAGE = 0

    VPD_MIN = 7.6
    MPD_MAX = 10.5

    def __init__(self, relays):
        super().__init__()
        self.relays = relays

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

    def make_bottle_full(self):
        self.relays.relay_turn_on(self.PUMP_RELAY_NUM)
        time.sleep(self.PUMP_DURATION)
        self.relays.relay_turn_off(self.PUMP_RELAY_NUM)
        logging.debug('Humidifier bottle updated')

    def adjust_humidify(self, current_temperature, current_humidity):
        if not current_temperature or not current_humidity:
            return False

        total_usage = self.__get_total_usage()
        logging.debug('Total humidifier usage: {}'.format(total_usage))

        if self.__is_need_more_water():
            self.make_bottle_full()
            self.__reset_total_usage()

        target_humidity = self.get_ideal_humidity(current_temperature)
        if not target_humidity:
            return None

        if current_humidity < target_humidity:
            self.relays.relay_turn_on(self.HUMIDIFIER_RELAY_NUM)
            self.__update_total_usage()
        else:
            self.relays.relay_turn_off(self.HUMIDIFIER_RELAY_NUM)

    def get_ideal_humidity(self, current_temperature):
        if not current_temperature:
            return None

        try:
            target_humidity_min, target_humidity_max = VDP_TEMPERATURE_HUMIDITY[int(current_temperature)]
            return target_humidity_min
        except KeyError:
            logging.error("Temperature {} is incorrect".format(current_temperature))
            return None
