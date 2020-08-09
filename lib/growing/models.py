from lib.db import BaseModel
from peewee import *


class Config(BaseModel):
    name = CharField(unique=True)


class Period(BaseModel):
    name = CharField()
    config = ForeignKeyField(Config, backref='periods')
    day_from = IntegerField()
    day_to = IntegerField()
    temperature = FloatField(default=25)
    humidity = FloatField(default=65)
    sunrise_start = TimeField(null=True)
    sunrise_stop = TimeField(null=True)
    sunset_start = TimeField(null=True)
    sunset_stop = TimeField(null=True)
    red_spectrum = BooleanField(default=False)

    class Meta:
        indexes = (
            (('day_from', 'day_to'), True),
        )
