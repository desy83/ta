from data.models import *
import json

# random world seed ...
WORLD_SEED = 1024

class ReadJson(object):
    def __init__(self, path):
        try:
            self.__json_data = open(path)
            self.data = json.load(self.__json_data)
        except Exception, e:
            print e

class User(object):
    def __init__(self, name, entity, char):
        self._username = name
        self.entity = entity
        self._items = []
        self._info = ''
        self.char = char

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def items(self):
        query = CharItem.select().where(CharItem.char == self.char)
        item_list = []
        for char_item in query:
            item_list.append(config.items[char_item.item.name])
        return item_list
        #return [config.items[char_item.item.name] for char_item in CharItem.get(CharItem.char == self.char)]

    @items.setter
    def items(self, value):
        item = Items.get(Items.name == value.name)
        try:
            char_item = CharItem.select().where((CharItem.char == self.char) & (CharItem.item == item))
            char_item.amount += 1
            char_item.save()
        except:
            CharItem.create(char=self.char, item=item, amount=1)

    def remove_items(self, items):
        for i in items:
            self._items.remove(i)

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def level(self):
        return self.char.level

    @level.setter
    def level(self, value):
        self.char.level = value
        self.char.save()

    @property
    def health(self):
        return self.char.health

    @health.setter
    def health(self, value):
        self.char.health = value
        self.char.save()

    @property
    def mana(self):
        return self.char.mana

    @mana.setter
    def mana(self, value):
        self.char.mana = value
        self.char.save()

    @property
    def strength(self):
        return self.char.strength

    @strength.setter
    def strength(self, value):
        self.char.strength = value
        self.char.save()

    @property
    def dexterity(self):
        return self.char.dexterity

    @dexterity.setter
    def dexterity(self, value):
        self.char.dexterity = value
        self.char.save()


class Item(object):
    def __init__(self, name, attributes):
        self.name = name
        self._readname = attributes['name']
        self._level = attributes['level']
        self._attributes = attributes['attributes']
        self._rate = attributes['rate']
        self._enemies = attributes['enemies']
        self._condition = attributes['condition']
        # FIXME: link to useable classes

    @property
    def readname(self):
        return self._readname

    @property
    def level(self):
        return self._level

    @property
    def attributes(self):
        return self._attributes

    @property
    def rate(self):
        return self._rate

    @property
    def enemies(self):
        return self._enemies

    @property
    def condition(self):
        return self._condition

class Enemy(object):
    def __init__(self, name,  attributes):
        self.name = name
        self._health = attributes['health']
        self._level = attributes['level']
        self._sign = attributes['sign']
        self._etype = attributes['type']

    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, value):
        self._health = value

    @property
    def level(self):
        return self._level

    @property
    def sign(self):
        return self._sign

    @property
    def etype(self):
        return self._etype

class Config(object):
    def __init__(self):
        self.enemies = {}
        self.items = {}

        # create db tables
        try:
            db.connect()
            db.create_tables([Users, Char, Items, CharItem])
        except Exception, e:
            print e

        # init enemies
        enemies = ReadJson('data/enemies.json').data
        for name, attributes in enemies.items():
            self.enemies[name] = Enemy(name, attributes)
        # init items
        items = ReadJson('data/items.json').data
        for name, attributes in items.items():
            self.items[name] = Item(name, attributes)

        if not Items.select().count():
            for key in items.keys():
                Items.create(name = key)

        @property
        def enemies(self):
            return self.enemies

config = Config()
