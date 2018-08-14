import sys
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QTableWidget, QTableWidgetItem, QScroller, QAbstractItemView, QLineEdit, QTextEdit, QListWidgetItem, QListWidget, QListView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt, pyqtSignal
import pickle
import json

# need to convert listwidget to textedit

# pyuic5 design code for UI
from chat_design import Ui_MainWindow
from message_window import Ui_Form

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


class MessageWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)






class send_thread(QThread):
    def __init__(self, socket, message, recipient):
        self.s = socket
        self.message = message
        super().__init__()

    def run(self):
        message = bytes(self.message, 'utf8')
        self.s.send(message)



class recv_thread(QThread):
    sig = pyqtSignal(dict)
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
                        else: # this is a legitamate message
                            self.sig.emit(data)

                    else: # user is trying to inject json into the app
                        raise json.decoder.JSONDecodeError # this will display the text to the screen
                except json.decoder.JSONDecodeError:
                    msg = packet.decode('utf8')
                    self.sig.emit(msg)




class client_ui(QMainWindow, Ui_MainWindow):
    online_users_sig = pyqtSignal(list)
    contacts = {}

    def __init__(self, my_username):
        super().__init__() # this runs Qmainwindows __init__ method
        self.username = my_username

        # setup the user interface from Designer
        self.setupUi(self)

        # setup the messageWidget
        number = self.stackedWidget.addWidget(MessageWidget())
        self.stackedWidget.setCurrentIndex(number)


        # place the focus on the textbox
        # so the cursor goes there automatically
        self.stackedWidget.widget(number).message_textEdit.setFocus()
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

        # this should be if error the nquit and run all this anyways if not error
        if self.socket_error == False:
            self.stackedWidget.widget(number).message_view.setText("Welcome to the chat server")
            self.s.send(bytes(self.username, 'utf8')) # server will reciev the username

            # recieving socket threads with connected signals
            self.thread_recv = recv_thread(self.s) # self.message_view)
            self.thread_recv.start()
            self.thread_recv.sig.connect(self.post_messages)
            self.thread_recv.sig2.connect(self.post_users)
            self.thread_recv.sig3.connect(self.remove_users)

        # connect signals to slots
        self.stackedWidget.widget(number).message_textEdit.returnPressed.connect(self.submit)
        self.contacts_listWidget.itemDoubleClicked.connect(self.double_click)


    def double_click(self, item):
        #list_index =  self.contacts_listWidget.indexFromItem(item).row()
        user_clicked = item.text()
        contacts = self.contacts
        if user_clicked in contacts.values(): # then the index already exists
            for i,k in contacts.items(): # {'index': username}
                if k == user_clicked:
                    self.stackedWidget.setCurrentIndex(i)
                    return
        index = self.stackedWidget.addWidget(MessageWidget()) # index number
        contacts[index] = user_clicked
        self.stackedWidget.setCurrentIndex(index)
        self.stackedWidget.widget(index).name_label.setText(user_clicked)


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




    def post_messages(self, message):
        print(message)
        # self.message_view.append(message)

    def submit(self):
        recipient = self.stackedWidget.currentIndex()
        message = self.message_textEdit.toPlainText()
        if self.socket_error == True:
            return
        elif not message.strip(): # removes whitespace & if no text
            return
        elif len(message) > 200:
            print("the message is too long")
            return
        else:
            self.thread_send = send_thread(self.s, message)
            self.thread_send.start()
            self.message_textEdit.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = client_ui()
    window.show()
    sys.exit(app.exec_())
