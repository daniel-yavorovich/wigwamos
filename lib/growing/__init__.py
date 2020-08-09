import logging
import re
import datetime
from .models import Config, Period
from ..properties import Property


class InvalidConfigName(Exception):
    pass


class ConfigNotFound(Exception):
    pass


class Growing(Property):
    START_GROWING_PROPERTY_KEY = 'start_growing_timestamp'
    CURRENT_GROWING_CONFIG_NAME = 'CURRENT_GROWING_CONFIG_NAME'
    DEFAULT_CONFIG_NAME = 'Autoflowering'

    def reset_day_counter(self):
        date = datetime.datetime.now()
        return self.set_property(self.START_GROWING_PROPERTY_KEY, str(date.timestamp()))

    def set_day_counter(self, day):
        date = datetime.datetime.now() - datetime.timedelta(days=day)
        return self.set_property(self.START_GROWING_PROPERTY_KEY, str(date.timestamp()))

    def get_start_growing_date(self):
        start_timestamp = self.get_property_value(self.START_GROWING_PROPERTY_KEY)
        if not start_timestamp:
            self.reset_day_counter()
            start_timestamp = self.get_property_value(self.START_GROWING_PROPERTY_KEY)

        return datetime.datetime.fromtimestamp(float(self.get_property_value(self.START_GROWING_PROPERTY_KEY)))

    def get_growing_day_count(self):
        return (datetime.datetime.now() - self.get_start_growing_date()).days + 1

    def __validate_config_name(self, name):
        pattern = re.compile(r'[A-Za-z0-9]+')
        if not name or not pattern.fullmatch(name):
            raise InvalidConfigName

    def config_dict_to_model(self, data):
        return Config(**data)

    def model_to_dict(self, model):
        return model.__dict__

    def create_config(self, data):
        name = data.get('name')

        self.__validate_config_name(name)

        if self.get_config(name):
            logging.warning('Config "{}" already imported'.format(name))
            return None

        config = Config.create(name=name)

        for period_data in data['periods']:
            Period.create(config=config, **period_data)

        return config

    def get_config(self, name):
        try:
            return Config.get(name=name)
        except Config.DoesNotExist:
            return None

    def get_config_names(self):
        return [c.name for c in Config.select()]

    def set_current_config(self, name):
        self.__validate_config_name(name)
        if name not in self.get_config_names():
            raise ConfigNotFound("Config {} not found".format(name))

        self.set_property(self.CURRENT_GROWING_CONFIG_NAME, name)

    def get_current_config_name(self):
        name = self.get_property_value(self.CURRENT_GROWING_CONFIG_NAME)
        if not name:
            self.set_current_config(self.DEFAULT_CONFIG_NAME)
            name = self.DEFAULT_CONFIG_NAME

        return name

    def get_current_config(self):
        return self.get_config(self.get_current_config_name())

    def get_current_period(self):
        config = self.get_current_config()
        day_count = self.get_growing_day_count()
        return config.periods.select().where(Period.day_from <= day_count, Period.day_to >= day_count).get()

    def get_growing_total_days(self):
        config = self.get_current_config()
        return config.periods.select().order_by('day_to')[-1].day_to
