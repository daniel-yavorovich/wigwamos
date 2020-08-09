from lib.db import db
from peewee import *


class Config(Model):
    name = CharField()

    class Meta:
        database = db


class Period(Model):
    name = CharField()
    period = ForeignKeyField(Config, backref='periods')
    day_from = IntegerField()
    day_to = IntegerField()
    temperature = FloatField()
    humidity = FloatField()
    sunrise_start = TimeField()
    sunrise_stop = TimeField()
    sunset_start = TimeField()
    sunset_stop = TimeField()
    red_spectrum = BooleanField()

    class Meta:
        database = db
