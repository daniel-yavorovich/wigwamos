from settings import SQLITE_DATABASE
from peewee import SqliteDatabase

db = SqliteDatabase(SQLITE_DATABASE)
