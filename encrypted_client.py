import sys
import os
from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget, QApplication, QTableWidget, QTableWidgetItem, QScroller, QAbstractItemView, QLineEdit, QTextEdit, QListWidgetItem, QListWidget, QListView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt, pyqtSignal

import configparser
import json



# pyuic5 design code for UI
from chat_design import Ui_MainWindow
from message_window import Ui_Form
from colors_diolog import Ui_Dialog

from colors import colors_ui

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import socket
from threading import Thread

import time

# # from sqlalchemy model created
# from model import Base, User

#
# #==============DB integration =================
# engine = create_engine('sqlite:///app.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
#
# # context manager for updating the database
# @contextmanager
# def session_update():
#     """Provide a transactional scope around a series of operations."""
#     session = DBSession()
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()
#
# # context manager for querying the database
# @contextmanager
# def session_query():
#     """Provide a transactional scope around a series of operations."""
#     session = DBSession()
#     yield session
#     session.close()
# #=========================================

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encrypt():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('chat.ini')

        password = config['Keys']['password']
        password = password.encode('utf-8') # needs to be in bytes
        salt = config['Keys']['salt']
        salt = salt.encode('utf-8') # converts the string into bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.f = Fernet(key)
        # print(key)
        #token = f.encrypt(b"Secret message!")
        #f.decrypt(token)
        #b'Secret message!

    def encrypt_message(self, message):
        message = message.encode('utf-8')
        token  = self.f.encrypt(message)
        return token

    def decrypt_message(self, token):
        message = self.f.decrypt(token)
        return message


class MessageWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class send_thread(QThread):
    # def __init__(self, socket, data):
    def __init__(self, socket, token):
        self.s = socket
        # self.message = json.dumps(data)
        self.token = token
        super().__init__()

    def run(self):

        # message = bytes(self.message, 'utf8')
        self.s.send(token)



class recv_thread(QThread):
    # sig = pyqtSignal(dict)
    sig = pyqtSignal(str)
    sig2 = pyqtSignal(list)
    sig3 = pyqtSignal(str)
    #sig4 = pyqtSignal(dict)
    def __init__(self, socket): # , message_view):
        self.s = socket
        #self.message_view = message_view
        super().__init__()

    def run(self):
        # data = b''
        while True:
            packet = self.s.recv(4096)
            # data += packet
            if not packet: # then the person has left
                break
            else:
                try:
                    data = json.loads(packet)
                    if isinstance(data, (list,)): # if contacts is a list
                        self.sig2.emit(data)
                    elif isinstance(data, (dict,)):
                        # if vlaue is False then the format is
                        # {username: False} single element dictionary
                        if False in data.values():
                            username = list(data.keys())[0]
                            self.sig3.emit(username)
                        # else: # this is a legitamate message
                        #     # format  is {username, message}
                        #     self.sig.emit(data)
                    else: # user is trying to inject json into the app (json can't load text)
                        raise json.decoder.JSONDecodeError # this will display the text to the screen
                except json.decoder.JSONDecodeError:
                    # msg = packet.decode('utf8') # turns bytes into str
                    # self.sig.emit(msg)
                    self.sig.emit(packet)



class client_ui(QMainWindow, Ui_MainWindow):
    online_users_sig = pyqtSignal(list)
    contacts = {}

    # colors for customization will change depending on when the user changes color
    config = configparser.ConfigParser()
    config.read("chat.ini")


    time_color = config['Colors']['time_color']
    username_color = config['Colors']['username_color']
    message_color = config['Colors']['message_color']
    background_color = config['Colors']['background_color']

    def __init__(self, my_username):
        super().__init__() # this runs Qmainwindows __init__ method
        self.username = my_username

        # setup the user interface from Designer
        self.setupUi(self)

        # setup the encryption class
        self.encryption = Encrypt()

        # setup the colors dialog
        self.customize_colors = colors_ui(client_ui.time_color, client_ui.username_color, client_ui.message_color, client_ui.background_color)

        # setup the messageWidget
        number = self.stackedWidget.addWidget(MessageWidget()) # returns index of 0
        self.stackedWidget.setCurrentIndex(number)

        # if clicked on colors: then show dialog
        self.actionColors.triggered.connect(self.show_colors_dialog)

        # place the focus on the textbox
        # so the cursor goes there automatically
        self.stackedWidget.widget(number).message_textEdit.setFocus() #index will be 0
        #self.message_textEdit.setFocus()


        # client socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 12345
        self.socket_error = False

        try:
            self.s.connect(("localhost", self.port))
        except socket.error: # catches the errors
            self.socket_error = True
            self.stackedWidget.widget(number).message_view.setText("Socket Connection Failed")
            time.sleep(3)
            self.s.close()
            print("you suck")

        # this should be if error the nquit and run all this anyways if not error
        if self.socket_error == False:
            self.s.sendall(bytes(self.username, 'utf8')) # server will recieve the username

            # recieving socket threads with connected signals
            self.thread_recv = recv_thread(self.s) # self.message_view)
            self.thread_recv.start()
            self.thread_recv.sig.connect(self.post_messages)
            self.thread_recv.sig2.connect(self.post_users)
            self.thread_recv.sig3.connect(self.remove_users)

        # colors_dialog connected signal
        self.customize_colors.sig_colors.connect(self.change_colors)


        # connect signals to slots
        self.stackedWidget.widget(number).message_textEdit.returnPressed.connect(self.submit)
        # self.contacts_listWidget.itemDoubleClicked.connect(self.double_click)

    # not doing private messages
    # def double_click(self, item):
    #     user_clicked = item.text()
    #     #contacts = self.contacts
    #     if user_clicked in self.contacts.values(): # then the index already exists
    #         for i,k in self.contacts.items(): # {'index': username}
    #             if k == user_clicked:
    #                 self.stackedWidget.setCurrentIndex(i)
    #                 return
    #     index = self.stackedWidget.addWidget(MessageWidget()) # index number
    #     self.contacts[index] = user_clicked
    #     # contacts[index] = user_clicked
    #     self.stackedWidget.setCurrentIndex(index)
    #     self.stackedWidget.widget(index).name_label.setText(user_clicked)
    #
    #     # connect signal to slot for new stackedWidget widget
    #     self.stackedWidget.widget(index).message_textEdit.returnPressed.connect(self.submit)

    def change_colors(self, colors_list):
        client_ui.time_color = colors_list[0]
        client_ui.username_color = colors_list[1]
        client_ui.message_color = colors_list[2]
        client_ui.background_color = colors_list[3]

    def show_colors_dialog(self):
        self.customize_colors.show()


    def post_users(self, users): # users is a list of strings ['username1', 'username2']
        #contacts = self.contacts # get the dictionary ready
        listed_users = [self.contacts_listWidget.item(i).text() for i in range(self.contacts_listWidget.count())]
        for user in users:
            if user not in listed_users and user != self.username:
                self.contacts_listWidget.addItem(user)


    def remove_users(self, username): # username is a str
        listwidgetitem = self.contacts_listWidget.findItems(username, Qt.MatchExactly)[0]
        row = self.contacts_listWidget.row(listwidgetitem)
        item =  self.contacts_listWidget.takeItem(row) # returns the item then we delete it
        del item


    # max len of message can be 93*3 = 279
    def post_messages(self, packet):
        # tyring to format the text not worth it
        #
        # MAX_LEN = 93
        # if len(message) > MAX_LEN and len(message) < 186:
        #     # 93 is the cutoff for the next line in qtextedit assuming monospace font
        #     """if the message[94] (one after the cutoff to the next line)
        #         is not a space then then the word that message[93] is apart of
        #         should go to the next line
        #     """
        #     if message[MAX_LEN-2].isspace() and message[MAX_LEN].isspace(): # one letter word
        #         # then the cutoff letter93 or message[92] is a one letter word
        #         m1 = message[:MAX_LEN].strip() # message[0 to 92]
        #         self.stackedWidget.widget(0).message_view.append(m1)
        #         string = ' ' * 22
        #         m2 = string + message[MAX_LEN:].strip()
        #         self.stackedWidget.widget(0).message_view.append(m2)
        #
        #
        #     elif message[MAX_LEN-1].isalnum() and message[MAX_LEN].isalnum(): # at least 2 letter word
        #         index = MAX_LEN-2
        #         while True:
        #             if message[index].isspace(): # if was 2 letter word
        #                 m1 = message[:index].strip()
        #                 self.stackedWidget.widget(0).message_view.append(m1)
        #                 string = ' ' * 22
        #                 m2 = string + message[index:].strip()
        #                 self.stackedWidget.widget(0).message_view.append(m2)
        #                 return
        #             else:
        #                 index = index - 1
        #
        #     else: # there is a space that matches perfectly with the end
        #         m1 = message[:MAX_LEN].strip()
        #         self.stackedWidget.widget(0).message_view.append(m1)
        #         string = ' ' * 22
        #         m2 = string + message[MAX_LEN:].strip()
        #         self.stackedWidget.widget(0).message_view.append(m2)
        #
        # else:
        #     if len(message) >186:
        #         print('it got here')
        #     self.stackedWidget.widget(0).message_view.append(message)
        timestamp = packet[-8:].decode('utf8')
        encrypted_message = packet[:-8]

        message = self.encryption.decrypt_message(encrypted_message)
        message = message.decode('utf8')



        # time_color = message[0]
        # username_color = message[1]
        # msg_color = message[2]
        # background_color = message[3]
        # msg = ' '.join(message[4:])

        # message = f"<html><span style='background-color:{background_color}'><font color='{time_color}'>[{time_recieved}] </font><font color='{username_color}'>{username}: </font><font color='{msg_color}'>{msg}</font></span></html>"



        self.stackedWidget.widget(0).message_view.append(message)


    # sending text in textedit to the send thread which sends to Server
    def submit(self):
        message = self.stackedWidget.widget(0).message_textEdit.toPlainText()
        if self.socket_error == True:
            # return
            if not message.strip():
                self.stackedWidget.widget(0).message_view.append(message)
                return
        elif not message.strip(): # removes whitespace & if no text
            return
        elif len(message) > 200:
            print("the message is too long")
            return
        else:
            msg = message.strip()
            colors = ' '.join([client_ui.time_color, client_ui.username_color, client_ui.message_color, client_ui.background_color])
            msg = ' '.join([colors, msg]) # format = 'timecolor namecolor msgcolor message'

            token = self.encryption.encrypt_message(msg)

            # start the sending thread
            self.thread_send = send_thread(self.s, token)
            self.thread_send.start()
            self.stackedWidget.widget(0).message_textEdit.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = client_ui()
    window.show()
    sys.exit(app.exec_())