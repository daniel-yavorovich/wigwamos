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
        day_count = self.growing.get_day_count()

        humidity, temperature = self.sensors.get_sensors_data()
        fan_speed_percent = self.fan.get_fan_speed_percent()
        light_brightness_percent = self.light.get_light_brightness_percent()
        soil_moisture = 'fine'  # TODO: need to implement
        water_level = 100  # TODO: need to implement
        progress_percentage = 1
        status = 'fine'

        self.adjust_fan(humidity, temperature)
        self.adjust_light(self.growing.is_day)
        self.metrics.update_metrics(day_count, humidity, temperature, fan_speed_percent, light_brightness_percent)

        self.screen.display_show_stats(status, day_count, progress_percentage, humidity, temperature, fan_speed_percent, soil_moisture, water_level)
