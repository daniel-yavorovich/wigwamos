import time


class Screen:
    SCREEN_SHOW_TIMEOUT = 30

    def __init__(self):
        pass

    def enable(self):
        # TODO: need implement
        return True

    def disable(self):
        # TODO: need implement
        return True

    def show(self, day_count, temperature, humidity):
        self.enable()

        # TODO: need implement

        time.sleep(self.SCREEN_SHOW_TIMEOUT)
        self.disable()
        return True
