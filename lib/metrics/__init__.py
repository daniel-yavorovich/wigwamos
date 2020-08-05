class Metrics:
    def __init__(self):
        pass

    def save_metric(self, key, value):
        # TODO: need to implement
        return True

    def update_metrics(self, day_count, humidity, temperature, fan_speed_percent, light_brightness_percent):
        self.save_metric('grow_days', day_count)
        self.save_metric('humidity', humidity)
        self.save_metric('temperature', temperature)
        self.save_metric('fan_speed_percent', fan_speed_percent)
        self.save_metric('light_brightness_percent', light_brightness_percent)
