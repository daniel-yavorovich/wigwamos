from settings import DATABASE
from playhouse.db_url import connect
from peewee import Model

db = connect(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db
