from ..properties import Property


class Fan(Property):
    FAN_SPEED_MIN = 50
    FAN_STEP_PERCENT = 5
    FAN_TRIAC_HAT_CHANNEL = 1
    FAN_SPEED_PROPERTY_KEY = 'fan_speed'

    def __init__(self, triac_hat):
        super().__init__()
        self.triac_hat = triac_hat

        self.set_fan_speed(self.get_fan_speed(), force=True)

    def get_fan_speed(self):
        return int(self.get_property_value(self.FAN_SPEED_PROPERTY_KEY))

    def set_fan_speed(self, value, force=False):
        if value < self.FAN_SPEED_MIN:
            value = self.FAN_SPEED_MIN
        elif value > 100:
            value = 100

        if self.get_fan_speed() == value and not force:
            return False

        self.set_property(self.FAN_SPEED_PROPERTY_KEY, str(value))

        if value == 0:
            self.triac_hat.disable_channel(self.FAN_TRIAC_HAT_CHANNEL)
            return True

        self.triac_hat.change_voltage(self.FAN_TRIAC_HAT_CHANNEL, value)
        self.triac_hat.enable_channel(self.FAN_TRIAC_HAT_CHANNEL)

        return True

    def adjust_fan(self, current_temperature):
        fan_speed_percent = self.FAN_SPEED_MIN

        if not current_temperature:
            return False

        if current_temperature > 20:
            fan_speed_percent += self.FAN_STEP_PERCENT

        if current_temperature > 22:
            fan_speed_percent += self.FAN_STEP_PERCENT

        if current_temperature > 24:
            fan_speed_percent += self.FAN_STEP_PERCENT

        if current_temperature > 26:
            fan_speed_percent += self.FAN_STEP_PERCENT

        if current_temperature > 28:
            fan_speed_percent += self.FAN_STEP_PERCENT

        if current_temperature > 30:
            fan_speed_percent = 100

        self.set_fan_speed(fan_speed_percent)
