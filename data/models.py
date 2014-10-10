from lib.peewee import *

db = SqliteDatabase('data/config.db')

class BaseModel(Model):
    #
    # data interface [{'field1': 'val1-1', 'field2': 'val1-2'}]
    #
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
    endurence = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField
    wisdom = IntegerField()
    knowledge = IntegerField()

class Races(BaseModel):
    name = CharField()
    healt = IntegerField()
    endurence = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField
    wisdom = IntegerField()
    knowledge = IntegerField()

class Char(BaseModel):
    user = ForeignKeyField(Users)
    charclass = ForeignKeyField(Classes)

class Sort(BaseModel):
    sort = CharField() #healtpot
    info = TextField()

class Items(BaseModel):
    name = CharField()
    sort = ForeignKeyField(Sort)

class CharItem(BaseModel):
    char = ForeignKeyField(Char)
    item = ForeignKeyField(Items)
    amount = IntegerField()
