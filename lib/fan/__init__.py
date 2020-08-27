import logging

from ..properties import Property


class Fan(Property):
    FAN_SPEED_MIN = 50
    FAN_STEP_PERCENT = 5
    FAN_TRIAC_HAT_CHANNEL = 1
    FAN_SPEED_PROPERTY_KEY = 'fan_speed'
    MANUAL_MODE_PROPERTY_KEY = 'fan_manual_mode'
    ALLOWED_TEMPERATURE_HESITATION = 0.7

    def init(self, triac_hat):
        self.set_fan_speed(triac_hat, self.get_fan_speed(), force=True)

    def get_fan_speed(self):
        return int(self.get_property_value(self.FAN_SPEED_PROPERTY_KEY))

    def set_fan_speed_property(self, value):
        self.set_property(self.FAN_SPEED_PROPERTY_KEY, str(value))

    def set_fan_speed(self, triac_hat, value, force=False):
        if value < self.FAN_SPEED_MIN:
            value = self.FAN_SPEED_MIN
        elif value > 100:
            value = 100

        if self.get_fan_speed() == value and not force and value != 0 and value != 100:
            return False

        self.set_fan_speed_property(value)

        if value == 0:
            logging.warning('Fan disabled!')
            triac_hat.disable_channel(self.FAN_TRIAC_HAT_CHANNEL)
            return True

        triac_hat.change_voltage(self.FAN_TRIAC_HAT_CHANNEL, value)
        triac_hat.enable_channel(self.FAN_TRIAC_HAT_CHANNEL)

        return True

    def set_manual_mode(self, value=False):
        if value:
            self.set_property(self.MANUAL_MODE_PROPERTY_KEY, True)
        else:
            self.delete_property(self.MANUAL_MODE_PROPERTY_KEY)

    def is_manual_mode(self):
        return bool(self.get_property_value(self.MANUAL_MODE_PROPERTY_KEY))

    def __temp_with_hesitation(self, temperature):
        return temperature - self.ALLOWED_TEMPERATURE_HESITATION, temperature + self.ALLOWED_TEMPERATURE_HESITATION

    def get_ideal_fan_speed(self, target_temperature, current_temperature):
        current_fan_speed = self.get_fan_speed()

        if current_temperature <= 16:
            return 0

        if current_temperature >= 30:
            return 100

        if current_fan_speed == 0:
            current_fan_speed = self.FAN_SPEED_MIN

        t_min, t_max = self.__temp_with_hesitation(current_temperature)
        if t_min > target_temperature and t_max > target_temperature:
            fan_speed = current_fan_speed + 1
        elif t_min < target_temperature and t_max < target_temperature:
            fan_speed = current_fan_speed - 1
        else:
            return current_fan_speed

        if fan_speed >= 100:
            return 100
        elif fan_speed <= self.FAN_SPEED_MIN:
            return self.FAN_SPEED_MIN
        else:
            return fan_speed

    def adjust_fan(self, triac_hat, target_temperature, current_temperature):
        if not current_temperature or not target_temperature or self.is_manual_mode():
            return False

        fan_speed_percent = self.get_ideal_fan_speed(target_temperature, current_temperature)
        self.set_fan_speed(triac_hat, fan_speed_percent)

    def get_all_info(self):
        return {
            'fan_speed': self.get_fan_speed(),
            'manual_mode': self.is_manual_mode()
        }
