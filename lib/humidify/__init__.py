import time
import datetime
import logging

from ..properties import Property


class Humidify(Property):
    HUMIDIFIER_RELAY_NUM = 2
    HUMIDIFY_DURATION = 30
    MAX_IDLE_HUMIDIFY_TIME = 300
    LAST_HUMIDIFY_PROPERTY_KEY = 'last_humidify_time'

    def __init__(self, relays):
        super().__init__()
        self.relays = relays

    def update_last_humidify_time(self):
        date = datetime.datetime.now()
        return self.set_property(self.LAST_HUMIDIFY_PROPERTY_KEY, str(date.timestamp()))

    def get_last_humidify_time(self):
        last_humidify_time = self.get_property_value(self.LAST_HUMIDIFY_PROPERTY_KEY)
        if not last_humidify_time:
            self.update_last_humidify_time()
            last_humidify_time = self.get_property_value(self.LAST_HUMIDIFY_PROPERTY_KEY)

        return datetime.datetime.fromtimestamp(float(last_humidify_time))

    def run_humidify(self, duration=HUMIDIFY_DURATION):
        time_from_last_humidify = (datetime.datetime.now() - self.get_last_humidify_time()).seconds
        if time_from_last_humidify < self.MAX_IDLE_HUMIDIFY_TIME:
            logging.warning('Need to wait {} seconds for the moisture is distributed'.format(
                self.MAX_IDLE_HUMIDIFY_TIME - time_from_last_humidify))
            return False

        self.relays.relay_turn_on(self.HUMIDIFIER_RELAY_NUM)
        time.sleep(duration)
        self.relays.relay_turn_off(self.HUMIDIFIER_RELAY_NUM)

        logging.info('Humidify completed after {} sec'.format(duration))

        self.update_last_humidify_time()

        return True

    def __is_need_humidify(self, period_humidity, avg_humidity):
        if avg_humidity is None:
            return False

        return period_humidity > avg_humidity

    def adjust_humidify(self, period, avg_humidity):
        if self.__is_need_humidify(period.humidity, avg_humidity):
            self.run_humidify()
