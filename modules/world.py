#
#   world.py
#
import random
from config import WORLD_SEED

ZONE_WIDTH = 80
ZONE_HEIGHT = 18

TILES = {
    0: ' ', 1: '#'
}

class World(object):
    def __init__(self):
        self._zones = {}
        pass

    def get_zone(self, x, y):
        zone_id = '%dx%d' % (x, y)
        zone = self._zones.get(zone_id)
        if not zone:
            zone = Zone(x, y)
            self._zones[zone_id] = zone
        return zone


class Entity(object):
    def __init__(self, x, y):
        pass


class Zone(object):
    def __init__(self, zone_x, zone_y):
        # entity list
        self._entities = []
        # map is constructed by a map using indices y*ZONE_WIDTH+x
        self._map = {}
        random.seed(WORLD_SEED * (zone_x + zone_y))
        self.clear()
        for x in range(ZONE_WIDTH):
            self.set(x, 0, 1)
            self.set(x, ZONE_HEIGHT-1, 1)
        for y in range(ZONE_HEIGHT):
            self.set(0, y, 1)
            self.set(ZONE_WIDTH-1, y, 1)
        for i in range(random.randint(20, 100)):
            self.set(random.randint(0, ZONE_WIDTH-1), random.randint(0, ZONE_HEIGHT-1), 1)
    def clear(self):
        for x in range(ZONE_WIDTH):
            for y in range(ZONE_HEIGHT):
                self.set(x, y, 0)
    def set(self, x, y, tile):
        self._map[y * ZONE_WIDTH + x] = tile
    def get(self, x, y):
        if (0 <= x < ZONE_WIDTH) and (0 <= y < ZONE_HEIGHT):
            return self._map[y * ZONE_WIDTH + x]
        else:
            return 0

    def render(self):
        data = []
        for y in range(ZONE_HEIGHT):
            for x in range(ZONE_WIDTH):
                data.append(TILES.get(self.get(x, y), ' '))
            data.append('\n')
        return ''.join(data)

