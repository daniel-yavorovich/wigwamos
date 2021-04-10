from datetime import datetime, timedelta

from lib.db import BaseModel
from peewee import *


class Config(BaseModel):
    name = CharField(unique=True)


class Period(BaseModel):
    name = CharField()
    config = ForeignKeyField(Config, backref='periods')
    day_from = IntegerField(unique=False)
    day_to = IntegerField(unique=False)
    temperature = FloatField(default=25)
    humidity = IntegerField()
    fan = IntegerField()
    sunrise = TimeField(null=True)
    day_length_hours = IntegerField(default=18)
    sunrise_duration_minutes = IntegerField(default=30)
    sunset_duration_minutes = IntegerField(default=30)
    red_spectrum = BooleanField(default=False)

    class Meta:
        indexes = (
            (('id', 'day_from', 'day_to'), True),
        )

    def is_sunrise_sunset_in_same_day(self):
        if not self.sunrise or not self.day_length_hours:
            return True
        return (self.sunrise.hour + self.day_length_hours) <= 24

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
        result = self.sunrise_datetime + timedelta(hours=self.day_length_hours)
        if not self.is_sunrise_sunset_in_same_day():
            result += timedelta(days=1)
        return result

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
