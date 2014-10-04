from lib.server import GameServer
import asyncore
import time

class VT100Codes:
    ESC = chr(27)
    JMPHOME = ESC+"[H"
    CLEARSCRN = ESC+"[2J"
    CLEARDOWN = ESC+"[J"

def tick(fps, last_time):
    interval = 60 / fps
    current_time = time.time()
    delta = current_time - last_time

    if delta < interval:
        time.sleep(interval - delta)

    return time.time()

game_server = GameServer('', 6900)

#NOTE game loop

while True:
    for addr,handler in game_server.connections.items():
        handler.send_data(VT100Codes.CLEARSCRN)
        handler.send_data(VT100Codes.JMPHOME)
        handler.send_data("TA-Server / Time: %s, Client: %s\n_____________________________________\nDwarf - Fritz - Fraz" % (time.strftime('%X'), addr[0]))
    asyncore.loop(
        timeout=0.1, count=1
    )
