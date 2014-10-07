class VT100Codes:
    ESC = chr(27)
    JMPHOME = ESC+"[H"
    CLEARSCRN = ESC+"[2J"
    CLEARDOWN = ESC+"[J"
