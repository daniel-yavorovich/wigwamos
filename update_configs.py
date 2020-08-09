#!/usr/bin/env python3
"""
Update configs in DB from local config dir
"""
import json
import os
import logging

from lib.properties import Property
from settings import LOG_LEVEL
from lib.growing import Growing

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'configs')


def update_configs():
    for c in os.listdir(CONFIG_PATH):
        with open(os.path.join(CONFIG_PATH, c)) as cf:
            model = growing.config_dict_to_model(json.load(cf))
            growing.create_config(model)
            logging.info('Config "{}" loaded'.format(model.name))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=LOG_LEVEL)
    prop = Property()
    growing = Growing(prop)

    update_configs()
