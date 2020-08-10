import time
import datetime
import logging

from ..properties import Property


class Watering(Property):
    WATERING_RELAY_NUM = 1
    WATERING_DURATION = 10
    MAX_IDLE_WATERING_TIME = 300
    LAST_WATERING_PROPERTY_KEY = 'last_watering_time'

    def __init__(self, relays):
        super().__init__()
        self.relays = relays

    def update_last_watering_time(self):
        date = datetime.datetime.now()
        return self.set_property(self.LAST_WATERING_PROPERTY_KEY, str(date.timestamp()))

    def get_last_watering_time(self):
        last_watering_time = self.get_property_value(self.LAST_WATERING_PROPERTY_KEY)
        if not last_watering_time:
            self.update_last_watering_time()
            last_watering_time = self.get_property_value(self.LAST_WATERING_PROPERTY_KEY)

        return datetime.datetime.fromtimestamp(float(last_watering_time))

    def run_watering(self, duration=WATERING_DURATION):
        time_from_last_watering = (datetime.datetime.now() - self.get_last_watering_time()).seconds
        if time_from_last_watering < self.MAX_IDLE_WATERING_TIME:
            logging.warning('Need to wait {} seconds for the water to drain'.format(
                self.MAX_IDLE_WATERING_TIME - time_from_last_watering))
            return False

        self.relays.relay_turn_on(self.WATERING_RELAY_NUM)
        time.sleep(duration)
        self.relays.relay_turn_off(self.WATERING_RELAY_NUM)

        logging.info('Watering completed after {} sec'.format(duration))

        self.update_last_watering_time()

        return True

    def adjust_fan(self, is_need_watering):
        if is_need_watering:
            self.run_watering()
