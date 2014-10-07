from modules.server import GameServer
from modules.render import Header, Auth
from lib.static import *
from config import *

import asyncore
import time

class GameMain(object):
    def __init__(self):
        self.game_server = game_server
        try:
            db.connect()
            #FIXME: create all necessary tables if not exists
            db.create_tables([Users])
        except Exception, e:
            print e

    def run(self):
        #NOTE game loop
        while True:
            for addr, handler in self.game_server.connections.items():
                handler.send_data(VT100Codes.CLEARSCRN)
                handler.send_data(VT100Codes.JMPHOME)

                if handler.auth:
                    handler.send_data(Header.write(addr))
                    handler.send_data(Auth.write())
                    # auth stuff
                else:
                    handler.send_data(Header.write(addr))
            asyncore.loop(timeout = 0.1, count = 1)

server = GameMain()
server.run()
