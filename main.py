from modules.server import GameServer
from lib.static import *
import asyncore
import time

game_server = GameServer('', 6900)

#NOTE game loop

while True:
    for addr,handler in game_server.connections.items():
        handler.send_data(VT100Codes.CLEARSCRN)
        handler.send_data(VT100Codes.JMPHOME)
        handler.send_data("TA-Server / Time: %s, Client: %s\n\r_____________________________________\n\rDwarf - Fritz - Fraz" % (time.strftime('%X'), addr[0]))
    asyncore.loop(
        timeout=0.1, count=1
    )
