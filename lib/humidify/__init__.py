from ..properties import Property


class Humidify(Property):
    HUMIDIFIER_RELAY_NUM = 1

    def __init__(self, relays):
        super().__init__()
        self.relays = relays

    def adjust_humidify(self, target_humidity, current_humidity):
        if current_humidity is None:
            return False

        if target_humidity > current_humidity:
            self.relays.relay_turn_on(self.HUMIDIFIER_RELAY_NUM)
        else:
            self.relays.relay_turn_off(self.HUMIDIFIER_RELAY_NUM)
