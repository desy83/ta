#
#   world.py
#
import random
from config import WORLD_SEED, config, Item, Enemy
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

    def fill(self, data):
        for x in range(self.width):
            for y in range(self.height):
                self.set_cell(x, y, data)

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
        if newx < 0:
            newx = ZONE_WIDTH - 1
            zonex = zonex - 1
        if newx >= ZONE_WIDTH:
            newx = 0
            zonex = zonex + 1
        if newy < 0:
            newy = ZONE_HEIGHT - 1
            zoney = zoney - 1
        if newy >= ZONE_HEIGHT:
            newy = 0
            zoney = zoney + 1
        # check collission
        if self._world.get_zone(zonex, zoney).collide(self, newx, newy):
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

    def damage(self, amount):
        if self.basis:
            if self.basis.health > amount:
                self.basis.health = self.basis.health - amount
                return True
            else:
                self._world.get_zone(self.zone_x, self.zone_y).remove_entity(self)
                drop_list = [item for item in config.items.keys() if self.basis.etype in config.items[item].enemies]
                drop_list = [config.items[item] for item in drop_list if config.items[item].rate >= random.randint(0, 100)]
                if drop_list:
                    item = random.choice(drop_list)
                    entity = self._world.add_entity(self.zone_x, self.zone_y, self.x, self.y, '+', copy(item))
                    self._world.get_zone(self.zone_x, self.zone_y).set_entity(entity)
                    self._world._items.append(item)
                    return True
                else:
                    return False
        else:
            return True

#
#   World abstraction
#
class World(object):
    def __init__(self):
        self._zones = {}
        self._enemies = []
        self._items = []
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

    def remove_entity(self, entity):
        self.get_zone(entity.zone_x, entity.zone_y).remove_entity(entity)


#
#   Zone abstraction
#
class Zone(object):
    def __init__(self, world, zone_x, zone_y):
        self.__set_seed(zone_x, zone_y)
        self._world = world
        self._tilemap = CellMap(ZONE_WIDTH, ZONE_HEIGHT)
        self._entitymap = CellMap(ZONE_WIDTH, ZONE_HEIGHT)

        self.generate2()

        for e in range(random.randint(0, 20)):
            enemy = config.enemies[random.choice(config.enemies.keys())]
            x = random.randint(1, ZONE_WIDTH-2)
            y = random.randint(1, ZONE_HEIGHT-2)
            if self._tilemap.get_cell(x, y):
                continue
            entity = self._world.add_entity(zone_x, zone_y, x, y, enemy.sign, copy(enemy))
            self.set_entity(entity)
            self._world._enemies.append(entity)

    def __set_seed(self, zone_x, zone_y):
        random.seed(WORLD_SEED * (zone_x + zone_y))

    def generate2(self):
        # drunken walk path connection stuff :)
        w2 = int(ZONE_WIDTH / 2)
        h2 = int(ZONE_HEIGHT / 2)
        cx = w2 + random.randint(-5, 5)
        cy = h2 + random.randint(-3, 3)
        sillyness = random.randint(8, 12)
        def connect(startx, starty, targetx, targety):
            x = startx
            y = starty
            while True:
                self._tilemap.set_cell(x, y, 255)
                if x > 2:
                    self._tilemap.set_cell(x-1, y, 255)
                if x < ZONE_WIDTH - 3:
                    self._tilemap.set_cell(x+1, y, 255)
                if y > 2:
                    self._tilemap.set_cell(x, y-1, 255)
                if y < ZONE_HEIGHT - 3:
                    self._tilemap.set_cell(x, y+1, 255)
                r = random.randint(0, sillyness)
                if r == 0:
                    if x < targetx:
                        x = x + 1
                    if x > targetx:
                        x = x - 1
                elif r == 1:
                    if y < targety:
                        y = y + 1
                    if y > targety:
                        y = y - 1
                else:
                    if r % 2:
                        x = x + random.choice((-1, 1))
                    else:
                        y = y + random.choice((-1, 1))
                x = min(max(x, 1), ZONE_WIDTH-2)
                y = min(max(y, 1), ZONE_HEIGHT-2)
                if self._tilemap.get_cell(x, y) == 0:
                    return
                if x == targetx and y == targety:
                    return

        def mark():
            for x in range(ZONE_WIDTH):
                for y in range(ZONE_HEIGHT):
                    if self._tilemap.get_cell(x, y) == 255:
                        self._tilemap.set_cell(x, y, 0)

        def drunken_walk(sx, sy, dx, dy):
            self._tilemap.set_cell(cx, cy, 0)
            for x in range(-1,2):
                for y in range(-1,2):
                    self._tilemap.set_cell(sx+x, sy+y, 0)
            connect(sx + dx, sy + dy, cx, cy)
            mark()

        # create 4 paths...
        self._tilemap.fill(1)
        drunken_walk(0, h2, 1, 0)
        drunken_walk(ZONE_WIDTH - 1, h2, -1, 0)
        drunken_walk(w2, 0, 0, 1)
        drunken_walk(w2, ZONE_HEIGHT -1, 0, -1)

    def generate1(self):
        for x in range(ZONE_WIDTH):
            self._tilemap.set_cell(x, 0, 1)
            self._tilemap.set_cell(x, ZONE_HEIGHT-1, 1)
        for y in range(ZONE_HEIGHT):
            self._tilemap.set_cell(0, y, 1)
            self._tilemap.set_cell(ZONE_WIDTH-1, y, 1)

        self._tilemap.set_cell(0, int(ZONE_HEIGHT / 2), 0)
        self._tilemap.set_cell(ZONE_WIDTH-1, int(ZONE_HEIGHT / 2), 0)
        self._tilemap.set_cell(int(ZONE_WIDTH / 2), 0, 0)
        self._tilemap.set_cell(int(ZONE_WIDTH / 2), ZONE_HEIGHT-1, 0)

        for i in range(10):
            cx = random.randint(0, ZONE_WIDTH-1)
            cy = random.randint(0, ZONE_HEIGHT-1)
            r = random.randint(2, 4)
            rsq = r * r
            for x in range(cx - r, cx + r + 1):
                for y in range(cy - r, cy + r + 1):
                    dx = cx - x
                    dy = cy - y
                    dist = dx * dx + dy * dy
                    if dist <= rsq:
                        self._tilemap.set_cell(x, y, 1)

    def collide(self, caller, x, y):
        if self._tilemap.get_cell(x, y) > 0:
            return True
        entity = self._entitymap.get_cell(x, y)
        if entity:
            if type(entity.basis) is Enemy:
                caller.basis.char.health = caller.basis.char.health - 1
                return entity.damage(1)
            elif type(entity.basis) is Item:
                caller.basis.items = [entity.basis]
                caller.basis.info = 'found %s' % entity.basis.readname
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

    def find_free_place(self):
        while True:
            x = random.randint(0, ZONE_WIDTH-1)
            y = random.randint(0, ZONE_HEIGHT-1)
            if self._tilemap.get_cell(x, y) == 0:
                if not self._entitymap.get_cell(x, y):
                    return x, y

