import socket
import time
import datetime
from threading import Thread
import pickle
import json

from cryptography.fernet import Fernet

KEY = '_FgHRC9Fo9Az9E---pbjL6tpyu5UtOXA5Q7L3hxlOdE='
#KEY_for_users =





class Server():
    key = bytes(KEY, 'utf8')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
            encrypted_username = clientsocket.recv(1024)
            username = self.decrypt_msg(encrypted_username).decode('utf8') # string

            self.connections_dict[username] = clientsocket

            print(f'{username} on {address} connected')

            # this is the first thing that should happen not concurrently
            self.new_connection(username)


            thread = Thread(target=self.handle_client, args=[clientsocket, address, username])
            thread.daemon = True
            thread.start()


    def handle_client(self, clientsocket, address, username):
        while True:
            data = clientsocket.recv(2048)

            if not data: # then socket is closed and person left
                print(username, "has disconnected")
                self.connections_dict.pop(username, None)

                msg = f'*server* grey grey grey white {username} has left the chat' # format is username timecolor unmecolor msgcolor bckgcolor message
                encrypted_message = self.encrypt_msg(msg)

                alert = {username : False} # then person has left chat
                for connection in self.connections_dict.values():
                    #
                    encrypted_json = self.encrypt_msg(json.dumps(alert))
                    connection.sendall(encrypted_json)
                    time.sleep(.1) # need break or else both merge together

                    connection.sendall(encrypted_message)

                clientsocket.close()
                break
            else:
                for connection in list(self.connections_dict.values()):
                    connection.sendall(data)


    # for every new connection notify that the person has joined the chat
    def new_connection(self, username):
        for connection in self.connections_dict.values():
            # send the updated users list
            encrypted_json = self.encrypt_msg(json.dumps(list(self.connections_dict.keys())))
            #connection.sendall(bytes(json.dumps(list(self.connections_dict.keys())), 'utf8'))
            connection.sendall(encrypted_json)
            time.sleep(.2)

            #send message
            msg = f'*server* grey grey grey white {username} has joined the chat' # format is username timecolor unmecolor msgcolor bckgcolor message
            encrypted_message = self.encrypt_msg(msg)

            connection.sendall(encrypted_message)

    def encrypt_msg(self, message):
        f = Fernet(Server.key)
        token = f.encrypt(bytes(message, 'utf8'))
        return token

    def decrypt_msg(self, token):
        f = Fernet(Server.key)
        message = f.decrypt(token) # message still in bytes
        return message



server = Server()
server.accept_clients()
