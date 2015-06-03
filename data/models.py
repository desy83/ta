from lib.peewee import *

db = SqliteDatabase('data/config.db')

class BaseModel(Model):
    # data interface [{'field1': 'val1-1', 'field2': 'val1-2'}]
    def init(self, models):
        for data in models:
            self.create(**data)
    class Meta:
        database = db

class Users(BaseModel):
    username = CharField(unique=True)
    password = CharField()

class Classes(BaseModel):
    name = CharField()
    health = IntegerField()
    mana = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()

class Races(BaseModel):
    name = CharField()
    health = IntegerField()
    mana = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()
    wisdom = IntegerField()

class Items(BaseModel):
    name = CharField()
    readname = CharField()
    level = IntegerField()
    health = IntegerField()
    mana = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()
    rate = IntegerField()
    enemies = CharField()
    condition = IntegerField()
    category = IntegerField()

class Char(BaseModel):
    user = ForeignKeyField(Users)
    #charclass = ForeignKeyField(Classes)
    #race = ForeignKeyField(Races)
    level = IntegerField()
    experience = IntegerField()
    #name = CharField()
    health = IntegerField()
    mana = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()
    zonex = IntegerField()
    zoney = IntegerField()

class CharItem(BaseModel):
    char = ForeignKeyField(Char)
    item = ForeignKeyField(Items)
    condition = IntegerField()
    equipped = BooleanField()
