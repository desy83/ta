class VT100Codes:
    ESC = chr(27)
    JMPHOME = ESC+"[H"
    CLEARSCRN = ESC+"[2J"
    CLEARDOWN = ESC+"[J"

def check_ascii(characters):
    check = True
    for c in characters:
        if ord(c) > 128:
            check = False
    return check
