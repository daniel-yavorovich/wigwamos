import logging
import datetime
from ..properties import Property


class Light(Property):
    LIGHT_RELAY_NUM = 0
    COOLER_RELAY_NUM = 2
    LIGHT_BRIGHTNESS_PROPERTY_KEY = 'light_brightness'

    def __init__(self):
        super().__init__()
        self.set_property(self.LIGHT_BRIGHTNESS_PROPERTY_KEY, '0')

    def get_light_brightness(self):
        return int(self.get_property_value(self.LIGHT_BRIGHTNESS_PROPERTY_KEY))

    def set_light_brightness(self, relays, value):
        self.set_property(self.LIGHT_BRIGHTNESS_PROPERTY_KEY, str(value))

        if value == 0:
            return self.light_power_off(relays)

        self.light_power_on(relays)

    def light_power_off(self, relays):
        relays.relay_turn_off(self.LIGHT_RELAY_NUM)
        relays.relay_turn_off(self.COOLER_RELAY_NUM)

    def light_power_on(self, relays):
        relays.relay_turn_on(self.LIGHT_RELAY_NUM)
        relays.relay_turn_on(self.COOLER_RELAY_NUM)

    def is_light_disabled(self, period):
        if not period.sunrise or not period.day_length_hours:
            return True

    def __get_time_diff(self, time_from, time_to):
        result = time_to - time_from
        return result.seconds

    def adjust_light(self, relays, period, is_high_temperature=False):
        now = datetime.datetime.now()

        if is_high_temperature:
            logging.warning('The light is off due to high temperature!')
            return self.set_light_brightness(relays, 0)

        if self.is_light_disabled(period):
            light_brightness = 0
        elif period.sunrise_datetime <= now <= period.sunset_datetime:
            seconds_from_sunrise_start = self.__get_time_diff(period.sunrise_datetime, now)
            light_brightness = 100 * seconds_from_sunrise_start / period.sunrise_duration_seconds
        elif period.sunset_datetime <= now <= period.sunrise_datetime:
            seconds_from_sunset_start = self.__get_time_diff(period.sunset_datetime, now)
            light_brightness = (-100 * seconds_from_sunset_start / period.sunset_duration_seconds) + 100
        else:
            light_brightness = 0

        if light_brightness > 100:
            light_brightness = 100

        light_brightness = int(light_brightness)

        if self.get_light_brightness() != light_brightness:
            return self.set_light_brightness(relays, light_brightness)
