from ..properties import Property


class Fan(Property):
    FAN_SPEED_MIN = 70
    FAN_UP_STEP_PERCENT = 5
    FAN_TRIAC_HAT_CHANNEL = 1
    FAN_SPEED_PROPERTY_KEY = 'fan_speed'

    def __init__(self, triac_hat):
        super().__init__()
        self.triac_hat = triac_hat

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

    def adjust_fan(self, humidity, temperature):
        # TODO: use table from https://xn----itbbja1ajgfecfvb9m.xn--p1ai/raznoe/optimalnaya-temperatura-v-groubokse-d-2kanna-biz-502-bad-gateway.html#i
        fan_speed_percent = self.FAN_SPEED_MIN

        if temperature > 20:
            fan_speed_percent += self.FAN_UP_STEP_PERCENT

        if temperature > 22:
            fan_speed_percent += self.FAN_UP_STEP_PERCENT

        if temperature > 24:
            fan_speed_percent += self.FAN_UP_STEP_PERCENT

        if temperature > 26:
            fan_speed_percent += self.FAN_UP_STEP_PERCENT

        if temperature > 28:
            fan_speed_percent += self.FAN_UP_STEP_PERCENT

        if temperature > 30:
            fan_speed_percent = 100

        self.set_fan_speed(fan_speed_percent)
