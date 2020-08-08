class Light:
    def __init__(self):
        pass

    def get_light_brightness_percent(self):
        # TODO: need to implement
        return 100

    def set_light_brightness_percent(self, value):
        # TODO: need to implement
        return True

    def light_power_off(self):
        # TODO: need to implement
        return True

    def light_power_on(self):
        # TODO: need to implement
        return True

    def sunrise(self, duration=None):
        """
        :param duration: Sunrise duration in seconds
        :return: result
        """
        if not duration or duration <= 0:
            return self.light_power_on()

        return True

    def sunset(self, duration=None):
        """
        :param duration: Sunrise duration in seconds
        :return: result
        """
        if not duration or duration <= 0:
            return self.light_power_off()

        return True

    def adjust_light(self, is_day):
        pass
