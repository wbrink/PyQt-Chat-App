import sys
import os
from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget, QApplication, QTableWidget, QTableWidgetItem, QScroller, QAbstractItemView, QLineEdit, QTextEdit, QListWidgetItem, QListWidget, QListView, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt, pyqtSignal

from colors_diolog import Ui_Dialog
import configparser


class colors_ui(QDialog, Ui_Dialog):
    # setup signal
    sig_colors = pyqtSignal(list)

    def __init__(self, time_color, username_color, message_color, background_color):
        super().__init__()


        # setup the user interface from Designer
        self.setupUi(self)

        # retrieve the html color names from file
        self.colors = []
        with open('colors/colors.txt', 'r') as f:
            for line in f.readlines():
                self.colors.append(line.strip().lower())

        self.time_comboBox.addItems(self.colors)
        self.username_comboBox.addItems(self.colors)
        self.message_comboBox.addItems(self.colors)
        self.background_comboBox.addItems(self.colors)


        self.time_color = time_color
        self.username_color = username_color
        self.message_color = message_color
        self.background_color = background_color

        # indexes for the combobox
        self.time_index = self.time_comboBox.findText(self.time_color)
        self.username_index = self.username_comboBox.findText(self.username_color)
        self.message_index = self.message_comboBox.findText(self.message_color)
        self.background_index = self.background_comboBox.findText(self.background_color)

        self.time_comboBox.setCurrentIndex(self.time_index)
        self.username_comboBox.setCurrentIndex(self.username_index)
        self.message_comboBox.setCurrentIndex(self.message_index)
        self.background_comboBox.setCurrentIndex(self.background_index)

        self.colors_buttonBox.rejected.connect(self.close) # closes the window
        self.colors_buttonBox.accepted.connect(self.customize)


    def customize(self):
        time_color = self.time_comboBox.currentText()
        username_color = self.username_comboBox.currentText()
        message_color = self.message_comboBox.currentText()
        background_color = self.background_comboBox.currentText()
        print(f"{time_color} {username_color} {message_color} {background_color}")
        colors_list = [time_color, username_color, message_color, background_color]

        # add the colors to the chat.ini file so that it saves preferences
        config = configparser.ConfigParser()
        config.read("chat.ini")

        # making changes to the config file so that the changes save
        config['Colors']['time_color'] = time_color
        config['Colors']['username_color'] = username_color
        config['Colors']['message_color'] = message_color
        config['Colors']['background_color'] = background_color

        # have to write the new changes to config file
        with open('chat.ini', 'w') as f:
            config.write(f)


        # emit signal
        self.sig_colors.emit(colors_list)



        self.close()
