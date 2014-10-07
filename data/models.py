from lib.peewee import *

db = SqliteDatabase('data/config.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    username = CharField(unique=True)
    password = CharField()
