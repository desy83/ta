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

        # iac wont linemode
        self.send("\377\375\042")
        # iac will suppress-goahead
        self.send("\377\373\3")
        # iac do suppress-goahead
        self.send("\377\375\3")


    def handle_read(self):
        data = self.recv(BUFFER_SIZE)
        if data:
            print '[%s] %s' % (self.__address[0], data)

    def send_data(self, data):
        self.send(data)


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

