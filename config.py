from data.models import *
from lib.static import Colors, set_color
import json

# random world seed ...
WORLD_SEED = 1024

# init attributes
ATTRIBUTES = {'level': 1, 'experience': 1, 'health': 10, 'mana': 10, 'strength': 10, 'dexterity': 10, 'zonex': 0, 'zoney': 0}

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
        self.maxhealth = ATTRIBUTES['health'] + char.level * 2
        self.maxmana = ATTRIBUTES['mana'] + char.level

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
            char_item = CharItem.get((CharItem.char == self.char) & (CharItem.item == item))
            char_item.amount += 1
            char_item.save()
        except:
            CharItem.create(char=self.char, item=item, amount=1)

    def remove_items(self, items):
        for i in items:
            self._items.remove(i)

    def item_amount(self, item):
        i = Items.get(Items.name == item.name)
        return CharItem.get((CharItem.char == self.char) & (CharItem.item == i)).amount

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
    def experience(self):
        return self.char.experience

    @experience.setter
    def experience(self, value):
        self.char.experience = value
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

    @property
    def zonex(self):
        return self.char.zonex

    @zonex.setter
    def zonex(self, value):
        self.char.zonex = value
        self.char.save()

    @property
    def zoney(self):
        return self.char.zoney

    @zoney.setter
    def zoney(self, value):
        self.char.zoney = value
        self.char.save()


class Item(object):
    def __init__(self, name, attributes):
        self._name = name
        self._readname = attributes['name']
        self._level = attributes['level']
        self._attributes = attributes['attributes']
        self._rate = attributes['rate']
        self._enemies = attributes['enemies']
        self._condition = attributes['condition']
        self._category = attributes['category']
        # FIXME: link to useable classes

    @property
    def name(self):
        return self._name

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

    @property
    def category(self):
        return self._category

class Enemy(object):
    def __init__(self, name,  attributes):
        self._name = name
        self._health = attributes['health']
        self._level = attributes['level']
        self._sign = attributes['sign']
        self._colored_sign = attributes['sign']
        self._etype = attributes['type']
        if self._etype in (3, ):
            self._colored_sign = set_color(self._sign, Colors.REDBOLD)

    @property
    def name(self):
        return self._name

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
    def colored_sign(self):
        return self._colored_sign

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
