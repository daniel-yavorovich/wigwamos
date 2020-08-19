import datetime
import time

import logging

from ..properties import Property


class Humidify(Property):
    HUMIDIFIER_RELAY_NUM = 1
    PUMP_RELAY_NUM = 3

    PUMP_DURATION = 3
    MAX_BOTTLE_CAPACITY = 120

    LAST_USAGE = datetime.datetime.now()
    TOTAL_USAGE = 0

    def __init__(self, relays):
        super().__init__()
        self.relays = relays

    def __update_last_usage(self):
        self.LAST_USAGE = datetime.datetime.now()

    def __get_last_usage(self):
        return self.LAST_USAGE

    def __update_total_usage(self):
        now = datetime.datetime.now()
        self.TOTAL_USAGE += (now - self.__get_last_usage()).seconds
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

    def adjust_humidify(self, target_humidity, current_humidity):
        if current_humidity is None:
            return False

        logging.debug('Total humidifier usage: {}'.format(self.__get_total_usage()))

        if self.__is_need_more_water():
            self.make_bottle_full()
            self.__reset_total_usage()

        if target_humidity > current_humidity:
            self.relays.relay_turn_on(self.HUMIDIFIER_RELAY_NUM)
            self.__update_total_usage()
        else:
            self.relays.relay_turn_off(self.HUMIDIFIER_RELAY_NUM)
