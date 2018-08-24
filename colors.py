import sys
import os
from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget, QApplication, QTableWidget, QTableWidgetItem, QScroller, QAbstractItemView, QLineEdit, QTextEdit, QListWidgetItem, QListWidget, QListView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt, pyqtSignal

from colors_diolog import Ui_Dialog


class colors_ui(QDialog, Ui_Dialog):
    def __init__(self, time_color, username_color, message_color):
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


        self.time_color = time_color
        self.username_color = username_color
        self.message_color = message_color

        # indexes for the combobox
        self.time_index = self.time_comboBox.findText(self.time_color)
        self.username_index = self.time_comboBox.findText(self.username_color)
        self.message_index = self.time_comboBox.findText(self.message_color)

        self.time_comboBox.setCurrentIndex(self.time_index)
        self.username_comboBox.setCurrentIndex(self.username_index)
        self.message_comboBox.setCurrentIndex(self.message_index)
