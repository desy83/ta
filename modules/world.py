#
#   world.py
#
import random
from config import WORLD_SEED, config
from copy import copy

ZONE_WIDTH = 48
ZONE_HEIGHT = 18

TILES = {
    0: ' ', 1: '#'
}

#
#   General purpose 2D map object
#
class CellMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._cells = {}

    def inboard(self, x, y):
        return (0 <= x < self.width) and (0 <= y < self.height)

    def get_cell(self, x, y):
        if self.inboard(x, y):
            return self._cells.get(y * self.width + x)
        else:
            return None

    def set_cell(self, x, y, data):
        if self.inboard(x, y):
            self._cells[y * self.width + x] = data

    def clear(self):
        self._cells = {}


#
#   Entity abstraction
#
class Entity(object):
    def __init__(self, world, zone_x, zone_y, x, y, tile, basis = None):
        self._world = world
        self.zone_x = zone_x
        self.zone_y = zone_y
        self.x = x
        self.y = y
        self.tile = tile
        self.basis = basis
        #self.move(0, 0) # link

    def render_world(self):
        return self._world.get_zone(self.zone_x, self.zone_y).render()

    def move(self, dx, dy):
        # calc new pos
        newx = self.x + dx
        newy = self.y + dy
        zonex = self.zone_x
        zoney = self.zone_y
        if newx < 1:
            newx = ZONE_WIDTH - 2
            zonex = zonex - 1
        if newx >= ZONE_WIDTH - 1:
            newx = 1
            zonex = zonex + 1
        if newy < 1:
            newy = ZONE_HEIGHT - 2
            zoney = zoney - 1
        if newy >= ZONE_HEIGHT - 1:
            newy = 1
            zoney = zoney + 1
        # check collission
        if self._world.get_zone(zonex, zoney).collide(newx, newy):
            return
        # unlink from old pos
        self._world.get_zone(self.zone_x, self.zone_y).remove_entity(self)
        # update pos
        self.x = newx
        self.y = newy
        self.zone_x = zonex
        self.zone_y = zoney
        # link to new pos
        self._world.get_zone(self.zone_x, self.zone_y).set_entity(self)


#
#   World abstraction
#
class World(object):
    def __init__(self):
        self._zones = {}
        self._enemies = []
        pass

    def get_zone(self, x, y):
        zone_id = '%dx%d' % (x, y)
        zone = self._zones.get(zone_id)
        if not zone:
            zone = Zone(self, x, y)
            self._zones[zone_id] = zone
        return zone

    def add_entity(self, zone_x, zone_y, x, y, tile = '@', basis = None):
        return Entity(self, zone_x, zone_y, x, y, tile, basis)


#
#   Zone abstraction
#
class Zone(object):
    def __init__(self, world, zone_x, zone_y):
        random.seed(WORLD_SEED * (zone_x + zone_y))
        self._world = world
        self._tilemap = CellMap(ZONE_WIDTH, ZONE_HEIGHT)
        self._entitymap = CellMap(ZONE_WIDTH, ZONE_HEIGHT)

        for x in range(ZONE_WIDTH):
            self._tilemap.set_cell(x, 0, 1)
            self._tilemap.set_cell(x, ZONE_HEIGHT-1, 1)
        for y in range(ZONE_HEIGHT):
            self._tilemap.set_cell(0, y, 1)
            self._tilemap.set_cell(ZONE_WIDTH-1, y, 1)
        for i in range(random.randint(20, 80)):
            self._tilemap.set_cell(random.randint(0, ZONE_WIDTH-1), random.randint(0, ZONE_HEIGHT-1), 1)
        for e in range(random.randint(0, 10)):
            enemy = config.enemies[random.choice(config.enemies.keys())]
            x = random.randint(1, ZONE_WIDTH-2)
            y = random.randint(1, ZONE_HEIGHT-2)
            if self._tilemap.get_cell(x, y):
                continue
            entity = self._world.add_entity(zone_x, zone_y, x, y, enemy.sign, copy(enemy))
            self.set_entity(entity)
            self._world._enemies.append(entity)

    def collide(self, x, y):
        if self._tilemap.get_cell(x, y) > 0:
            return True
        entity = self._entitymap.get_cell(x, y)
        if entity:
            if entity.basis:
                if entity.basis.health > 1:
                    entity.basis.health = entity.basis.health-1
                    return True
                else:
                    self.remove_entity(entity)
                    return False
            else:
                return True
        return False

    def render(self):
        data = []
        for y in range(ZONE_HEIGHT):
            for x in range(ZONE_WIDTH):
                entity = self._entitymap.get_cell(x, y)
                if entity:
                    data.append(entity.tile)
                else:
                    data.append(TILES.get(self._tilemap.get_cell(x, y), ' '))
            data.append('\n')
        return ''.join(data)

    def remove_entity(self, entity):
        self._entitymap.set_cell(entity.x, entity.y, None)

    def set_entity(self, entity):
        self._entitymap.set_cell(entity.x, entity.y, entity)

