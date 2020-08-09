#!/usr/bin/env python3

from lib.growing.models import db, Config, Period

db.create_tables([Config, Period])
