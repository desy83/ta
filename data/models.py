from lib.peewee import *

db = SqliteDatabase('data/config.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    username = CharField(unique=True)
    password = CharField()

class Classes(BaseModel):
    name = CharField()
    health = IntegerField()    
    mana = IntegerField()       # for skills
    strength = IntegerField()   # more dmg meele
    dexterity = IntegerField()    # more dmg range
    wisdom = IntegerField()     # more dmg mage

class Races(BaseModel):
    name = CharField()
    health = IntegerField()
    mana = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()
    wisdom = IntegerField()

class Char(BaseModel):
    user = ForeignKeyField(Users)
    charclass = ForeignKeyField(Classes)
    race = ForeignKeyField(Races)
    level = IntegerField()
    # absolute values of the char (combined char, race and levelup values)
    name = CharField()
    health = IntegerField()
    mana = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField()
    wisdom = IntegerField()

class Sort(BaseModel):
    sort = CharField() #healpot
    info = CharField()

class Items(BaseModel):
    name = CharField()
    sort = ForeignKeyField(Sort)

class CharItem(BaseModel):
    char = ForeignKeyField(Char)
    item = ForeignKeyField(Items)
    amount = IntegerField()
   
