import socket
import time
from threading import Thread
import pickle
import json

class Server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connections_dict = {} # dictionary with username as key socket as value

    HOST = 'localhost'
    PORT = 12345

    def __init__(self):
        self.s.bind((self.HOST,self.PORT))
        self.s.listen(3)
        accept = Thread(target=self.accept_clients) # no args
        accept.daemon = True
        accept.start()
        #accept.join()
        #self.s.close()

    def accept_clients(self):
        while True:
            # establish a connection
            clientsocket, address = self.s.accept()

            print(str(address[0]), "on port:", str(address[1]), "connected")
            username = clientsocket.recv(1024).decode('utf8')

            self.connections_dict[username] = clientsocket
            print(self.connections_dict)


            print(username, 'connected')

            # this is the first thing that should happen not concurrently
            self.new_connection(username)


            thread = Thread(target=self.handle_client, args=[clientsocket, address, username])
            thread.daemon = True
            thread.start()

    def handle_client(self, clientsocket, address, username):
        while True:
            data = clientsocket.recv(1024)

            if not data: # then socket is closed and person left
                print(username, "has disconnected")
                self.connections_dict.pop(username, None)
                for connection in self.connections_dict.values():
                    alert = {username : False} # then person has left chat
                    #connection.send(bytes("{} has left the chat".format(username), 'utf8'))
                    connection.send(bytes(json.dumps(alert), 'utf8'))

                clientsocket.close()
                break
            else: # then messages will be sent
                post = json.loads(data) #
                if isinstance(post, (dict,)):
                    for connection, msg in post.items() # {recipient: message, etc.}
                        if connection == clientsocket:
                            msg = '<html><font color="red">{}:</font> {}</html>'.format(username, msg)
                        else:
                            msg = '<html><font color="blue">{}:</font> {}</html>'.format(username, msg)
                        connection.send(bytes(msg, 'utf8'))


    # for every new connection notify that the person has joined the chat
    def new_connection(self, username):
        for connection in self.connections_dict.values():
            connection.send(bytes(json.dumps(list(self.connections_dict.keys())), 'utf8'))





server = Server()
server.accept_clients()
