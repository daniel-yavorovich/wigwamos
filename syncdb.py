#!/usr/bin/env python3

from lib.db import db
from lib.growing.models import Config, Period
from lib.properties.models import Property


def sync_database():
    db.create_tables([Config, Period, Property])


if __name__ == '__main__':
    sync_database()
