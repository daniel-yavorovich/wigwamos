from peewee import *
from lib.db import db


class Property(Model):
    key = CharField(unique=True)
    value = TextField()

    class Meta:
        database = db
