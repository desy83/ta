from config import *
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
    @staticmethod
    def write(user):
        data = '\nEquipment:\n'
        equipment = []
        potion = []
        for item in user.items:
            if item.category == 0:
                equipment.append((item, user.item_amount(item)))
            elif item.category == 1:
                potion.append((item, user.item_amount(item)))

        data += ', '.join([e[0].readname + ' ' + str(e[1]) + 'x' for e in equipment])

        return data


