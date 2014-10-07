from config import *
import time

class RenderBase(object):
    def __init__(self):
        pass

    def write(self, data):
        pass

    def read(self):
        pass

class Header(RenderBase):
    @staticmethod
    def write(data):
       return "TA-Server / Time: %s, Client: %s\n\r______________________________________________\n\r" % (time.strftime('%X'), data[0])
    def read(self):
        pass

class Auth(RenderBase):
    @staticmethod
    def write():
        return 'username: '

