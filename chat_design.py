# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat_design.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(925, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.contacts_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.contacts_listWidget.setGeometry(QtCore.QRect(10, 30, 161, 441))
        self.contacts_listWidget.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.contacts_listWidget.setObjectName("contacts_listWidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(190, 10, 721, 461))
        self.stackedWidget.setObjectName("stackedWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 925, 22))
        self.menubar.setObjectName("menubar")
        self.menuAdd_Contact = QtWidgets.QMenu(self.menubar)
        self.menuAdd_Contact.setObjectName("menuAdd_Contact")
        self.menuhello = QtWidgets.QMenu(self.menubar)
        self.menuhello.setObjectName("menuhello")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Contact = QtWidgets.QAction(MainWindow)
        self.actionNew_Contact.setObjectName("actionNew_Contact")
        self.actionColors = QtWidgets.QAction(MainWindow)
        self.actionColors.setObjectName("actionColors")
        self.menuAdd_Contact.addAction(self.actionNew_Contact)
        self.menuhello.addAction(self.actionColors)
        self.menubar.addAction(self.menuhello.menuAction())
        self.menubar.addAction(self.menuAdd_Contact.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuAdd_Contact.setTitle(_translate("MainWindow", "Contact"))
        self.menuhello.setTitle(_translate("MainWindow", "Customize"))
        self.actionNew_Contact.setText(_translate("MainWindow", "New Contact"))
        self.actionColors.setText(_translate("MainWindow", "Colors"))

