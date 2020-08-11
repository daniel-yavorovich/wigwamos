import logging

from ..properties import Property


class Fan(Property):
    FAN_SPEED_MIN = 70
    FAN_STEP_PERCENT = 5
    FAN_TRIAC_HAT_CHANNEL = 1
    FAN_SPEED_PROPERTY_KEY = 'fan_speed'

    def __init__(self, triac_hat):
        super().__init__()
        self.triac_hat = triac_hat

        self.set_fan_speed(self.FAN_SPEED_MIN)

    def get_fan_speed(self):
        return int(self.get_property_value(self.FAN_SPEED_PROPERTY_KEY))

    def set_fan_speed(self, value):
        if value < self.FAN_SPEED_MIN:
            value = self.FAN_SPEED_MIN
        elif value > 100:
            value = 100

        self.set_property(self.FAN_SPEED_PROPERTY_KEY, str(value))

        if value == 0:
            self.triac_hat.disable_channel(self.FAN_TRIAC_HAT_CHANNEL)
            return True

        self.triac_hat.change_voltage(self.FAN_TRIAC_HAT_CHANNEL, value)
        self.triac_hat.enable_channel(self.FAN_TRIAC_HAT_CHANNEL)

        return True

    def adjust_fan(self, period, temperature):
        fan_speed_percent_old = fan_speed_percent = self.get_fan_speed()

        if not temperature:
            return False

        if period.temperature < temperature:
            fan_speed_percent += self.FAN_STEP_PERCENT
        elif period.temperature > temperature:
            fan_speed_percent -= self.FAN_STEP_PERCENT

        if fan_speed_percent_old != fan_speed_percent:
            self.set_fan_speed(fan_speed_percent)

        return True
