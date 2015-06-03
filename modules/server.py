from modules.render import Header, Auth, Welcome, Inventory
from config import *
from lib.static import *

import asyncore
import socket
import time

BUFFER_SIZE = 8192
CONNECTION_SIZE = 5

class GameHandler(asyncore.dispatcher_with_send):
    def __init__(self, (connection, address), world, server):
        asyncore.dispatcher_with_send.__init__(self, connection)
        self.__address = address
        self.__last_called = float()
        self.server = server
        self.user = None
        self.userobject = None
        self.shutdown = False
        self.username = None
        self.password = None
        self.state = States.AUTH
        self.run = False
        self.authstep = 0
        self.world = world
        self.entity = None
        self.send(Welcome.write(address))
        self.send(Auth.username())
        self.last_time = time.time()
        self.inventory = Inventory()

    def tick(self):
        current_time = time.time()
        delta = current_time - self.last_time
        #NOTE: current one second, make it more granular
        if delta > 60:
            self.run = True
            self.last_time = current_time


    def set_char_mode(self, mode=True):
        if mode:
            # iac wont linemode
            self.send("\377\375\042")
            # iac will suppress-goahead
            self.send("\377\373\3")
            # iac do suppress-goahead
            self.send("\377\375\3")
        else:
            # iac will linemode
            self.send("\377\373\042")
            # iac wont suppress-goahead
            self.send("\377\375\3")
            # iac dont suppress-goahead
            self.send("\377\376\3")

    def handle_read(self):
        data = self.recv(BUFFER_SIZE)
        if data:
            datastrip = data.strip()
            if self.state == States.AUTH:
                if check_ascii(datastrip) and len(datastrip) <= 8:
                    if self.authstep == 0:
                        try:
                            self.userobject = Users.get(Users.username == datastrip)
                            self.username = self.userobject.username
                            self.password = self.userobject.password
                            self.send(Auth.password())
                        except:
                            self.username = datastrip
                            self.send(Auth.newpassword())
                        self.authstep = 1
                    elif self.authstep == 1:
                        if self.password and self.password == datastrip:
                            char = Char.get(Char.user == self.userobject)
                            self.state = States.WORLD
                            self.set_char_mode(True)
                            px, py = self.world.get_zone(char.zonex, char.zoney).find_free_place()
                            self.entity = self.world.add_entity(char.zonex, char.zoney, px, py, set_color("@", Colors.YELLOWBOLD)) # player entity
                            self.world.get_zone(char.zonex, char.zoney).set_entity(self.entity)
                            self.user = User(self.username, self.entity, char)
                            self.entity.basis = self.user
                        elif self.password and self.password <> datastrip:
                            self.authstep = 0
                            self.password = None
                            self.send(Auth.error('wrong password'))
                            self.send(Auth.username())
                        else:
                            try:
                                #FIXME: get attributs from classes and races
                                user = Users.create(username=self.username, password=datastrip)
                                char = Char.create(user = user, level=ATTRIBUTES['level'], experience=ATTRIBUTES['experience'], health=ATTRIBUTES['health'], mana=ATTRIBUTES['mana'], strength=ATTRIBUTES['strength'], dexterity=ATTRIBUTES['dexterity'], zonex=ATTRIBUTES['zonex'], zoney=ATTRIBUTES['zoney'])
                                self.state = States.WORLD
                                self.set_char_mode(True)
                                px, py = self.world.get_zone(char.zonex, char.zoney).find_free_place()
                                self.entity = self.world.add_entity(char.zonex, char.zoney, px, py, set_color("@", Colors.YELLOWBOLD)) # player entity
                                self.world.get_zone(char.zonex, char.zoney).set_entity(self.entity)
                                self.user = User(self.username, self.entity, char)
                                self.entity.basis = self.user
                            except Exception, e:
                                print e
                else:
                    self.authstep = 0
                    self.password = None
                    self.send(Auth.error('incorrect input'))
                    self.send(Auth.username())

            else:
                key = datastrip
                if key in ('\x1b^['):
                    self.handle_close()
                # World Keyset
                if self.state == States.WORLD:
                    if key in ('w', 'W', '\x1b[A'):
                        self.entity.move(0, -1)
                    elif key in ('s', 'S', '\x1b[B'):
                        self.entity.move(0, 1)
                    elif key in ('a', 'A', '\x1b[D'):
                        self.entity.move(-1, 0)
                    elif key in ('d', 'D', '\x1b[C'):
                        self.entity.move(1, 0)
                    elif key in ('i', 'I'):
                        self.state = States.INVENTORY
                        #item_list = []
                        #for item in self.user.items:
                        #    item_list.append(item.readname)
                        #self.user.info = ', '.join(item_list)
                # Inventory Keyset
                elif self.state == States.INVENTORY:
                    if key in ('i', 'I'):
                        self.state = States.WORLD
                    elif key in ('\x1b[A'):
                        self.inventory.selected_index -= 1
                    elif key in ('\x1b[B'):
                        self.inventory.selected_index += 1

                self.server.run_all_handler()

            self.run = True
            #print '[%s] %s' % (self.__address[0], datastrip)

    def send_data(self, data):
        self.send(data)

    def handle_close(self):
        self.world.remove_entity(self.entity)
        self.shutdown = True
        self.server.run_all_handler()
        self.close()

class GameServer(asyncore.dispatcher):

    def __init__(self, host, port, world):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(CONNECTION_SIZE)
        self.handler = None
        self.connections = dict()
        self.world = world

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            self.connections[addr] = GameHandler(pair, self.world, self)

    def run_all_handler(self):
        for handler in self.connections.values():
            handler.run = True

    def handle_close(self):
        self.close()
