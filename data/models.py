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
    endurence = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField
    wisdom = IntegerField()
    knowledge = IntegerField()

class Races(BaseModel):
    name = CharFiled()
    healt = IntegerField()
    endurence = IntegerField()
    strength = IntegerField()
    dexterity = IntegerField
    wisdom = IntegerField()
    knowledge = IntegerField()

class Skills(BaseModel):
    name = CharField()
    info = TextField()
        

class Char(BaseModel):
	class = ForeignKeyField(Classes)
    race = ForeignKeyField(Races)
    
    
