import time
import datetime
import logging

from ..properties import Property


class Watering(Property):
    WATERING_RELAY_NUM = 3
    WATERING_STEP_DURATION = 6
    WATERING_MAX_DURATION = 600
    WATERING_IN_PROGRESS_PROPERTY_KEY = 'watering_in_progress'

    def __init__(self, sensors, relays):
        super().__init__()
        self.sensors = sensors
        self.relays = relays

    def is_watering_in_progress(self):
        timestamp_text = self.get_property_value(self.WATERING_IN_PROGRESS_PROPERTY_KEY)

        if not timestamp_text:
            return False

        timestamp = float(timestamp_text)
        if (datetime.datetime.now() - datetime.datetime.fromtimestamp(timestamp)).seconds > self.WATERING_MAX_DURATION:
            return False

        return True

    def set_watering_in_progress(self):
        now = datetime.datetime.now()
        self.set_property(self.WATERING_IN_PROGRESS_PROPERTY_KEY, now.timestamp())

    def unset_watering_in_progress(self):
        self.delete_property(self.WATERING_IN_PROGRESS_PROPERTY_KEY)

    def is_need_watering(self, soil_moisture):
        if self.is_watering_in_progress() or soil_moisture is None:
            return False

        return soil_moisture == 1

    def run_watering(self):
        start_time = datetime.datetime.now()

        self.set_watering_in_progress()
        self.relays.relay_turn_on(self.WATERING_RELAY_NUM)

        while self.sensors.get_soil_moisture() == 1:
            time.sleep(self.WATERING_STEP_DURATION)

        self.relays.relay_turn_off(self.WATERING_RELAY_NUM)
        self.unset_watering_in_progress()

        stop_time = datetime.datetime.now()

        duration = (stop_time - start_time).seconds
        logging.info('Watering completed after {} sec'.format(duration))

        return True

    def adjust_watering(self, soil_moisture):
        if self.is_need_watering(soil_moisture):
            self.run_watering()
