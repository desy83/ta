from modules.render import Header, Auth, Welcome
from config import *

import asyncore
import socket
import time

BUFFER_SIZE = 8192
CONNECTION_SIZE = 5

class GameHandler(asyncore.dispatcher_with_send):
    def __init__(self, (connection, address)):
        asyncore.dispatcher_with_send.__init__(self, connection)
        self.__address = address
        self.__last_called = float()
        self.shutdown = False
        self.username = None
        self.password = None
        self.auth = False
        self.run = False
        self.authstep = 0
        self.send(Welcome.write(address))
        self.send(Auth.username())

    def set_char_mode(self, mode=True):
        if mode:
            # iac wont linemode
            self.send("\377\375\042")
            # iac will suppress-goahead
            self.send("\377\373\3")
            # iac do suppress-goahead
            self.send("\377\375\3")
        else:
            # iac will linemode
            self.send("\377\373\042")
            # iac wont suppress-goahead
            self.send("\377\375\3")
            # iac dont suppress-goahead
            self.send("\377\376\3")

    def handle_read(self):
        data = self.recv(BUFFER_SIZE)
        if data:
            datastrip = data.strip()
            if not self.auth:
                if self.authstep == 0:
                    try:
                        user = Users.get(Users.username == datastrip)
                        self.username = user.username
                        self.password = user.password
                        self.send(Auth.password())
                    except:
                        self.username = datastrip
                        self.send(Auth.newpassword())
                    self.authstep = 1
                elif self.authstep == 1:
                    if self.password and self.password == datastrip:
                        self.auth = True
                        self.set_char_mode(True)
                    elif self.password and self.password <> datastrip:
                        self.authstep = 0
                        self.password = None
                        self.send(Auth.error('wrong password'))
                        self.send(Auth.username())
                    else:
                        try:
                            Users.create(username=self.username, password=datastrip)
                            self.auth = True
                            self.set_char_mode(True)
                        except Exception, e:
                            print e
            self.run = True
            print '[%s] %s' % (self.__address[0], data)

    def send_data(self, data):
        self.send(data)

    def handle_close(self):
        self.close()
        self.shutdown = True

class GameServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(CONNECTION_SIZE)
        self.handler = None
        self.connections = dict()

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            self.connections[addr] = GameHandler(pair)

    def handle_close(self):
        self.close()
