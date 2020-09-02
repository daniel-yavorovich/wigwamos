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
        if not period.sunrise_start and not period.sunrise_start and not period.sunrise_start and not period.sunrise_start:
            return True

    def __get_time_diff(self, time_from, time_to):
        today = datetime.date.today()
        result = datetime.datetime.combine(today, time_to) - datetime.datetime.combine(today, time_from)
        return result.seconds

    def adjust_light(self, relays, period, is_high_temperature=False):
        now = datetime.datetime.now().time()

        if is_high_temperature:
            logging.warning('The light is off due to high temperature!')
            return self.set_light_brightness(relays, 0)

        if self.is_light_disabled(period):
            light_brightness = 0
        elif period.sunrise_start <= now <= period.sunset_start:
            if now < period.sunrise_stop:
                total_sunrise_seconds = self.__get_time_diff(period.sunrise_start, period.sunrise_stop)
                seconds_from_sunrise_start = self.__get_time_diff(period.sunrise_start, now)
                light_brightness = 100 * seconds_from_sunrise_start / total_sunrise_seconds
            else:
                light_brightness = 100
        elif period.sunset_start <= now <= period.sunrise_start:
            if now < period.sunset_stop:
                total_sunset_seconds = self.__get_time_diff(period.sunset_start, period.sunset_stop)
                seconds_from_sunset_start = self.__get_time_diff(period.sunset_start, now)
                light_brightness = (-100 * seconds_from_sunset_start / total_sunset_seconds) + 100
            else:
                light_brightness = 0
        else:
            light_brightness = 0

        light_brightness = int(light_brightness)

        if self.get_light_brightness() != light_brightness:
            return self.set_light_brightness(relays, light_brightness)
