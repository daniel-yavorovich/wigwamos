#!/usr/bin/env python3
import json
import os
import logging

from settings import LOG_LEVEL
from lib.growing import Growing
from syncdb import sync_database

CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'configs')


def update_configs():
    for c in os.listdir(CONFIG_PATH):
        with open(os.path.join(CONFIG_PATH, c)) as cf:
            config = growing.create_config(json.load(cf))
            logging.info('Config "{}" created'.format(config.name))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=LOG_LEVEL)
    growing = Growing()

    sync_database()
    update_configs()
