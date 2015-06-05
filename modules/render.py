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
        self.selected_index = -3
        self.equipment = []
        self.potion = []
        self.equipped = {}
        self.data = None
        self.item_count = 0
        self.info_text = None

    def fetch_item_count(self, user):
        self.item_count = user.items_amount()

    def __render_items(self):
        self.data = '\nCharacter:\n'
        for _, e in self.equipped.items():
            if e[0] == self.selected_index:
                self.data += e[2] % (set_background_text('%s\n' % (e[1].item.readname,) if e[1] else 'None\n', BgColors.RED),)
            else:
                self.data += e[2] % ('%s\n' % (e[1].item.readname,) if e[1] else 'None\n',)
        self.data += '\nEquipment:\n'
        #items = []
        #item_break = 0
        if not self.equipment:
            self.data += 'None\n'
        else:
            for e in self.equipment:
                '''
                item_break += len(e[1].item.readname) + 5
                if item_break > 40:
                    item_break_symbol = '\n'
                else:
                    item_break_symbol = ''
                '''
                if e[0] == self.selected_index:
                    self.data += set_background_text('%sx %s\n' % (str(e[2]), e[1].item.readname), BgColors.RED)
                else:
                    self.data += '%sx %s\n' % (str(e[2]), e[1].item.readname)
            #self.data += ', '.join(items)
        self.data += '\nPotions:\n'
        #items = []
        if not self.potion:
            self.data += 'None\n'
        else:
            for e in self.potion:
                if e[0] == self.selected_index:
                    self.data += set_background_text('%sx %s\n' % (str(e[2]), e[1].item.readname), BgColors.RED)
                else:
                    self.data += '%sx %s\n' % (str(e[2]), e[1].item.readname)
            #self.data += ', '.join(items)

    def get_selected_charitem(self):

        if self.selected_index == -3:
            return (ItemSection.EQUIPPED, self.equipped.get('armor')[1])
        elif self.selected_index == -2:
            return (ItemSection.EQUIPPED, self.equipped.get('weapon')[1])
        elif self.selected_index == -1:
            return (ItemSection.EQUIPPED, self.equipped.get('jewelry')[1])
        else:
            for e in self.equipment:
                if self.selected_index == e[0]:
                    return (ItemSection.EQUIPMENT, e[1])
            for e in self.potion:
                if self.selected_index == e[0]:
                    return (ItemSection.POTION, e[1])
        return (None, None)

    def write(self, user):
        self.equipment = []
        self.potion = []
        self.equipped = {}
        for index, char_item in enumerate(user.get_items_by_categories([0, 1, 2])):
            self.equipment.append((index, char_item, user.item_amount(char_item)))
        for index, char_item in enumerate(user.get_items_by_categories([3]), len(self.equipment)):
            self.potion.append((index, char_item, user.item_amount(char_item)))

        self.item_count = len(self.equipment) + len(self.potion)

        self.equipped['armor'] = (-3, user.get_equipped_item_by_category(1), '   O\t Armor: %s')
        self.equipped['weapon'] = (-2, user.get_equipped_item_by_category(0), ' /=Y=\ \t Weapon: %s')
        self.equipped['jewelry'] = (-1, user.get_equipped_item_by_category(2), '  / \ \t Jewelry: %s')

        self.__render_items()
        len_equipment = len(self.equipment) if len(self.equipment) else 1
        len_potion = len(self.potion) if len(self.potion) else 1
        line_breaks = (9-(len_equipment+len_potion))*'\n'
        if self.info_text:
            self.data += '%s%s' % (line_breaks, self.info_text)
            self.info_text = None
        else:
            _, selected_charitem = self.get_selected_charitem()
            if selected_charitem:
                self.data += '%sL:%s, C:%s, H:%s, M:%s, S:%s, D:%s' % (line_breaks, selected_charitem.item.level, selected_charitem.item.condition, selected_charitem.item.health, selected_charitem.item.mana, selected_charitem.item.strength, selected_charitem.item.dexterity)

        return self.data


