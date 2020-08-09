from lib.db import BaseModel
from peewee import *


class Config(BaseModel):
    name = CharField(unique=True)


class Period(BaseModel):
    name = CharField()
    config = ForeignKeyField(Config, backref='periods')
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
        indexes = (
            (('day_from', 'day_to'), True),
        )
