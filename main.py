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
            db.create_tables([Users, Classes, Races, Char])
        except Exception, e:
            print e

    def run(self):
        #NOTE game loop
        while True:
            for addr, handler in self.game_server.connections.items():

                if handler.auth:
                    handler.send_data(VT100Codes.CLEARSCRN)
                    handler.send_data(VT100Codes.JMPHOME)
                    handler.send_data(Header.write(addr))
                    handler.send_data(OnlineUsers.write(self.game_server.connections.values()))
            asyncore.loop(timeout = 0.1, count = 1)

server = GameMain()
server.run()
