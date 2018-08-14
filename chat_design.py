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
        MainWindow.resize(755, 492)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.contacts_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.contacts_listWidget.setGeometry(QtCore.QRect(10, 30, 181, 401))
        self.contacts_listWidget.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.contacts_listWidget.setObjectName("contacts_listWidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(220, 10, 511, 431))
        self.stackedWidget.setObjectName("stackedWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 755, 22))
        self.menubar.setObjectName("menubar")
        self.menuAdd_Contact = QtWidgets.QMenu(self.menubar)
        self.menuAdd_Contact.setObjectName("menuAdd_Contact")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Contact = QtWidgets.QAction(MainWindow)
        self.actionNew_Contact.setObjectName("actionNew_Contact")
        self.menuAdd_Contact.addAction(self.actionNew_Contact)
        self.menubar.addAction(self.menuAdd_Contact.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuAdd_Contact.setTitle(_translate("MainWindow", "Contact"))
        self.actionNew_Contact.setText(_translate("MainWindow", "New Contact"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

