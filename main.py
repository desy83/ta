from modules.server import GameServer
from lib.static import *
from config import *

import asyncore
import time

class GameMain(object):
    def __init__(self):
        self.game_server = GameServer('', 6900)
        try:
            db.connect()
            #FIXME: create all necessary tables if not exists
            db.create_tables([Users])
        except Exception, e:
            print e

    def run(self):
        #NOTE game loop
        while True:
            for addr,handler in self.game_server.connections.items():
                handler.send_data(VT100Codes.CLEARSCRN)
                handler.send_data(VT100Codes.JMPHOME)
                handler.send_data("TA-Server / Time: %s, Client: %s\n\r_____________________________________\n\rDwarf - Fritz - Fraz" % (time.strftime('%X'), addr[0]))
            asyncore.loop(timeout = 0.1, count = 1)

server = GameMain()
server.run()
