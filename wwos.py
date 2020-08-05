from lib.fan import Fan
from lib.growing import Growing
from lib.light import Light
from lib.screen import Screen
from lib.sensors import Sensors
from lib.metrics import Metrics


class WigWamOS:
    def __init__(self):
        self.fan = Fan()
        self.growing = Growing()
        self.light = Light()
        self.screen = Screen()
        self.sensors = Sensors()
        self.metrics = Metrics()

    def adjust_fan(self, humidity, temperature):
        pass

    def adjust_light(self, is_day):
        pass

    def run(self):
        alerts = []
        day_count = self.growing.get_day_count()

        humidity, temperature = self.sensors.get_humidity_temperature()
        need_watering = self.sensors.is_need_watering()
        fan_speed_percent = self.fan.get_fan_speed_percent()
        light_brightness_percent = self.light.get_light_brightness_percent()

        water_level = 100  # TODO: need to implement
        progress_percent = 1  # TODO: need to implement
        status = 'fine'  # TODO: need to implement

        self.adjust_fan(humidity, temperature)
        self.adjust_light(self.growing.is_day)
        self.metrics.update_metrics(day_count, humidity, temperature, fan_speed_percent, light_brightness_percent)

        if need_watering:
            alerts.append("NEED WATERING!")

        self.screen.display_show_stats(alerts, day_count, progress_percent, humidity, temperature, fan_speed_percent)

        return [day_count, humidity, temperature, fan_speed_percent, light_brightness_percent]
