from config import *
import time

class RenderBase(object):
    def __init__(self):
        pass

    def write(self, data):
        pass

    def read(self):
        pass

class Welcome(RenderBase):
    @staticmethod
    def write(data):
        return '''
                Welcome %s to TA-MUD
                Please Login and have fun
                ''' % (data[0],)

class Header(RenderBase):
    @staticmethod
    def write(data):
       return "TA-Server / Time: %s, Client: %s\n\r______________________________________________\n\r" % (time.strftime('%X'), data[0])
    def read(self):
        pass

class Auth(RenderBase):
    @staticmethod
    def username():
        return 'username: '

    @staticmethod
    def password():
        return 'password: '

    @staticmethod
    def newpassword():
        return 'new password: '
