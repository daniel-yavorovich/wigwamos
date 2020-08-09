from ..properties import Property


class Light(Property):
    LIGHT_RELAY_NUM = 0
    LIGHT_BRIGHTNESS_PROPERTY_KEY = 'light_brightness'

    def __init__(self, relays):
        super().__init__()
        self.relays = relays
        self.set_property(self.LIGHT_BRIGHTNESS_PROPERTY_KEY, '0')

    def get_light_brightness(self):
        return int(self.get_property_value(self.LIGHT_BRIGHTNESS_PROPERTY_KEY))

    def set_light_brightness(self, value):
        self.set_property(self.LIGHT_BRIGHTNESS_PROPERTY_KEY, str(value))

        if value == 0:
            return self.light_power_off()

        self.light_power_on()

    def light_power_off(self):
        self.relays.relay_turn_off(self.LIGHT_RELAY_NUM)

    def light_power_on(self):
        self.relays.relay_turn_on(self.LIGHT_RELAY_NUM)
