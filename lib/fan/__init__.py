from ..properties import Property
from ..triac_hat import TriacHat


class Fan(Property):
    FAN_TRIAC_HAT_CHANNEL = 1
    FAN_SPEED_PROPERTY_KEY = 'fan_speed'

    def __init__(self):
        super().__init__()
        self.triac_hat = TriacHat()

        self.set_property(self.FAN_SPEED_PROPERTY_KEY, '0')

    def get_fan_speed(self):
        return int(self.get_property_value(self.FAN_SPEED_PROPERTY_KEY))

    def set_fan_speed(self, value):
        self.set_property(self.FAN_SPEED_PROPERTY_KEY, str(value))

        if value == 0:
            self.triac_hat.disable_channel(self.FAN_TRIAC_HAT_CHANNEL)
            return

        self.triac_hat.change_voltage(self.FAN_TRIAC_HAT_CHANNEL, value)

        self.triac_hat.enable_channel(self.FAN_TRIAC_HAT_CHANNEL)
