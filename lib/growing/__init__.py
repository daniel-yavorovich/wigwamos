import re
import json
import datetime
from .models import Config, Period


class InvalidConfigName(Exception):
    pass


class ConfigNotFound(Exception):
    pass


class Growing:
    START_GROWING_PROPERTY_KEY = 'start_growing_timestamp'

    def __init__(self, prop):
        self.prop = prop

    def reset_day_counter(self):
        return self.prop.set_property(self.START_GROWING_PROPERTY_KEY, str(datetime.datetime.now().timestamp()))

    def get_start_growing_date(self):
        start_timestamp = self.prop.get_property_value(self.START_GROWING_PROPERTY_KEY)
        if not start_timestamp:
            self.reset_day_counter()
            start_timestamp = self.prop.get_property_value(self.START_GROWING_PROPERTY_KEY)

        return datetime.datetime.fromtimestamp(float(self.prop.get_property_value(self.START_GROWING_PROPERTY_KEY)))

    def get_growing_day_count(self):
        return (datetime.datetime.now() - self.get_start_growing_date()).days

    @property
    def is_day(self):
        # TODO: need implement
        return True

    def __validate_config_name(self, name):
        pattern = re.compile(r'[A-Za-z0-9]+')
        if not pattern.fullmatch(name):
            raise InvalidConfigName

    def __get_prop_name(self, name):
        return 'CONFIG_{}'.format(name)

    def config_dict_to_model(self, data):
        return Config(**data)

    def model_to_dict(self, model):
        return model.__dict__

    def create_config(self, model):
        self.__validate_config_name(model.name)
        self.prop.set_property(self.__get_prop_name(model.name), json.dumps(self.model_to_dict(model)))

    def get_config(self, name):
        data = self.prop.get_property_value(self.__get_prop_name(name))
        if not data:
            return None
        return self.config_dict_to_model(json.loads(data))

    def update_configs_list(self, names):
        self.prop.set_property('CONFIGS_LIST', json.dumps(names))

    def get_configs_list(self):
        data = self.prop.get_property_value('CONFIGS_LIST')
        if not data:
            return []
        return json.loads(data)

    def set_current_config(self, name):
        self.__validate_config_name(name)
        if name not in self.get_configs_list():
            raise ConfigNotFound("Config {} not found".format(name))

        self.prop.set_property('CURRENT_CONFIG', name)

    def get_current_config_name(self):
        return self.prop.get_property_value('CURRENT_CONFIG')

    def get_current_config(self):
        name = self.get_current_config_name()
        return self.get_config(name)