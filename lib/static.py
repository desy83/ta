ESC = chr(27)

class States:
    AUTH = 0
    WORLD = 1
    INVENTORY = 2
    LOGOUT = 3

class VT100Codes:
    JMPHOME = ESC+"[H"
    CLEARSCRN = ESC+"[2J"
    CLEARDOWN = ESC+"[J"

class Colors:
    REDBOLD = ESC+"[1;31m"
    RED = ESC+"[0;31m"
    YELLOWBOLD = ESC+"[1;33m"
    YELLOW = ESC+"[0;33m"
    GREENBOLD = ESC+"[1;32m"
    GREEN = ESC+"[0;32m"
    BLUEBOLD = ESC+"[1;34m"
    BLUE = ESC+"[0;34m"
    RESET = ESC+"[0m"

class BgColors:
    RED = ESC+"[0;41m"

def set_color(tile, color):
    return color+tile+Colors.RESET

def set_background_text(text, color):
    return color+text+Colors.RESET

def check_ascii(characters):
    check = True
    for c in characters:
        if ord(c) > 128:
            check = False
    return check
