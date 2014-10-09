from modules.server import GameServer
from modules.render import Header, Auth, OnlineUsers
from lib.static import *
from modules.server import GameServer
from config import *

import asyncore
import time

class GameMain(object):
    def __init__(self):
        self.game_server = GameServer('', 6900)
        try:
            db.connect()
            #FIXME: create all necessary tables if not exists
            db.create_tables([Users, Classes, Races, Char, Items, CharItem, Sort])
        except Exception, e:
            print e

    def run(self):
        #NOTE game loop
        while True:
            new_connections = {}
            for addr, handler in self.game_server.connections.items():
                if handler.shutdown:
                    del handler
                    continue
                new_connections[addr] = handler
                if handler.auth and self.run:
                    handler.send_data(VT100Codes.CLEARSCRN)
                    handler.send_data(VT100Codes.JMPHOME)
                    handler.send_data(Header.write(addr))
                    handler.send_data(OnlineUsers.write(self.game_server.connections.values()))
                    handler.run = False
            self.game_server.connections = new_connections
            asyncore.loop(timeout = 0.1, count = 1)

server = GameMain()
server.run()
