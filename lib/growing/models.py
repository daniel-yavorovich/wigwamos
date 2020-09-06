from datetime import datetime, timedelta

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
    sunrise = TimeField(null=True)
    day_length_hours = IntegerField(default=18)
    sunrise_duration_minutes = IntegerField(default=30)
    sunset_duration_minutes = IntegerField(default=30)
    red_spectrum = BooleanField(default=False)

    class Meta:
        indexes = (
            (('day_from', 'day_to'), True),
        )

    @property
    def sunrise_datetime(self):
        if not self.sunrise:
            return None
        today = datetime.today()
        return datetime.combine(today, self.sunrise)

    @property
    def sunset_datetime(self):
        if not self.sunrise:
            return None
        return self.sunrise_datetime + timedelta(hours=self.day_length_hours)

    @property
    def sunrise_duration_seconds(self):
        if not self.sunrise_duration_minutes:
            return 0
        return self.sunrise_duration_minutes * 60

    @property
    def sunset_duration_seconds(self):
        if not self.sunset_duration_minutes:
            return 0
        return self.sunset_duration_minutes * 60
