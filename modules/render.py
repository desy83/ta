from config import *
from lib.static import *
import time

LINE = '\n\r------------------------------------------------\n\r'

class RenderBase(object):
    def __init__(self):
        pass

    def write(self, data):
        pass

    def read(self):
        pass

class Welcome(RenderBase):
    @staticmethod
    def write(data):
        return '\n### Welcome %s to TA-MUD ###\n### Please Login and have fun ###\n\n' % (data[0],)

class Header(RenderBase):
    @staticmethod
    def write(data):
       return "TA-Server / Time: %s, Client: %s" % (time.strftime('%H:%M'), data[0]) + LINE
    def read(self):
        pass

class Auth(RenderBase):
    @staticmethod
    def username():
        return 'username: '

    @staticmethod
    def password():
        return 'password: '

    @staticmethod
    def newpassword():
        return 'new password: '

    @staticmethod
    def error(data):
        return '\nError: %s\n\n' % (data,)

class Error(RenderBase):
    @staticmethod
    def error(data):
       pass

class OnlineUsers(RenderBase):
    @staticmethod
    def write(handlers):
        users = []
        for handler in handlers:
            if handler.username and handler.state and not handler.shutdown:
                users.append(handler.username)
        users.sort()
        return 'Online Users: ' + ' '.join(users) + LINE

class Character(RenderBase):
    @staticmethod
    def write(handler):
        return 'C:W R:D / H:%s M:%s S:%s D:%s / L:%s / X:%s/Y:%s\n' % (handler.user.char.health, handler.user.char.mana, handler.user.char.strength, handler.user.char.dexterity, handler.user.char.level, handler.entity.zone_x, handler.entity.zone_y)

class Info(RenderBase):
    @staticmethod
    def write(user):
        b = user.info
        user.info = ''
        return '%s' % b

class Inventory(RenderBase):

    def __init__(self):
        self.selected_index = 0
        self.equipment = []
        self.potion = []
        self.equipped = []
        self.data = None

    def __render_hero(self):
        return '  O\t Armor: %s\n' % () + ' /=Y=\\tWeapon: %s\n' % () + '  / \\tJewelry: %s\n' % ()

    def __render_items(self):
        self.data += '\nEquipped:\n'
        for e in self.equipped:
            if e[0] == self.selected_index:
                self.data += set_background_text(e[1].item.readname if e[1] else 'None\n', BgColors.RED)
            else:
                self.data += e[1].item.readname if e[1] else 'None\n'
        self.data += '\nEquipment:\n'
        for e in self.equipment:
            if e[0] == self.selected_index:
                self.data += set_background_text('%s %s\n' % (str(e[2]), e[1].item.readname), BgColors.RED)
            else:
                self.data += '%s %s\n' % (str(e[2]), e[1].item.readname)
        self.data += '\nPotions:\n'
        for e in self.potion:
            if e[0] == self.selected_index:
                self.data += set_background_text('%s %s\n' % (str(e[2]), e[1].item.readname), BgColors.RED)
            else:
                self.data += '%s %s\n' % (str(e[2]), e[1].item.readname)


    def write(self, user):
        self.equipment = []
        self.potion = []
        self.equipped = []
        self.data = '\nInventory:\n'
        for index, char_item in enumerate(user.items):
            if char_item.item.category in [0, 1, 2]:
                self.equipment.append((index, char_item, user.item_amount(char_item)))
            elif char_item.item.category == 3:
                self.potion.append((index, char_item, user.item_amount(char_item)))

        #data += ', '.join([e[0].item.readname + ' ' + str(e[1]) + 'x' for e in equipment])
        self.equipped.append((-3, user.get_equipped_armor()))

        self.__render_items()

        return self.data


