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

class Enemie(object):
    def __init__(self, name,  attribues):
        self.name = name
        self._health = attribues['health']
        self._level = attribues['level']
        self._sign = attribues['sign']
        self._etype = attribues['type']

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
        # init enemies
        enemies = ReadJson('data/enemies.json').data
        for name, attributes in enemies.items():
            self.enemies[name] = Enemie(name, attributes)

        @property
        def enemies(self):
            return self.enemies

config = Config()
