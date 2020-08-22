import logging
from pyowm import OWM
from settings import OPENWEATHERMAP_API_KEY, OPENWEATHERMAP_LOCATION


class Weather:
    def __init__(self):
        self.owm = OWM(OPENWEATHERMAP_API_KEY)
        self.mgr = self.owm.weather_manager()

    def get_humidity_temperature(self):
        try:
            observation = self.mgr.weather_at_place(OPENWEATHERMAP_LOCATION)
            w = observation.weather
            return w.humidity, w.temperature('celsius')['temp']
        except Exception as e:
            logging.error(e)
            return None, None
