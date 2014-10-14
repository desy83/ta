from modules.server import GameServer
from modules.render import Header, Auth, OnlineUsers, Character, Info
from lib.static import *
from modules.server import GameServer
from modules.world import World
from config import *

import asyncore
import time

class GameMain(object):
    def __init__(self):
        self.world = World()
        self.game_server = GameServer('', 6900, self.world)

    def run(self):
        #NOTE game loop
        while True:
            new_connections = {}
            for addr, handler in self.game_server.connections.items():
                handler.tick()
                if handler.shutdown:
                    del handler
                    continue
                new_connections[addr] = handler
                if handler.auth and handler.run:
                    handler.send_data(VT100Codes.CLEARSCRN)
                    handler.send_data(VT100Codes.JMPHOME)
                    handler.send_data(Header.write(addr))
                    handler.send_data(OnlineUsers.write(self.game_server.connections.values()))
                    handler.send_data(Character.write(handler))
                    handler.send_data(handler.entity.render_world())
                    handler.send_data(Info.write(handler.user))
                    handler.run = False
            self.game_server.connections = new_connections
            asyncore.loop(timeout = 0.1, count = 1)

server = GameMain()
server.run()

