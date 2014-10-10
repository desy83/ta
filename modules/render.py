from config import *
import time

LINE = '\n\r------------------------------------------------\n\r'

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
        return '\n### Welcome %s to TA-MUD ###\n### Please Login and have fun ###\n\n' % (data[0],)

class Header(RenderBase):
    @staticmethod
    def write(data):
       return "TA-Server / Time: %s, Client: %s" % (time.strftime('%X'), data[0]) + LINE
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

    @staticmethod
    def error(data):
        return '\nError: %s\n\n' % (data,)

class Error(RenderBase):
    @staticmethod
    def error(data):
       pass

class OnlineUsers(RenderBase):
    @staticmethod
    def write(handlers):
        users = []
        for handler in handlers:
            if handler.username and handler.auth:
                users.append(handler.username)
        return 'Online Users: ' + ' '.join(users) + LINE
