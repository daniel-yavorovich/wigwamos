from lib.fan import Fan
from lib.growing import Growing
from lib.light import Light
from lib.screen import Screen
from lib.sensors import Sensors
from lib.metrics import Metrics


class WigWamOS(Fan, Growing, Light, Screen, Sensors, Metrics):

    def microclimate_setting(self, humidity, temperature):
        pass

    def light_setting(self, is_day):
        pass

    def update_metrics(self, day_count, humidity, temperature, fan_speed_percent):
        self.save_metric('grow_days', day_count)
        self.save_metric('humidity', humidity)
        self.save_metric('temperature', temperature)
        self.save_metric('fan_speed_percent', fan_speed_percent)

    def run(self):
        day_count = self.get_day_count()
        humidity, temperature = self.get_sensors_data()
        fan_speed_percent = self.get_fan_speed_percent()

        self.microclimate_setting(humidity, temperature)
        self.light_setting(self.is_day)
        self.update_metrics(day_count, humidity, temperature, fan_speed_percent)
