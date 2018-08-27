# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colors_diolog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 191)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 9, 261, 141))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(13)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.time_comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.time_comboBox.setObjectName("time_comboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.time_comboBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.username_comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.username_comboBox.setObjectName("username_comboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.username_comboBox)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.message_comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.message_comboBox.setObjectName("message_comboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.message_comboBox)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.background_comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.background_comboBox.setObjectName("background_comboBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.background_comboBox)
        self.colors_buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.colors_buttonBox.setGeometry(QtCore.QRect(100, 160, 166, 25))
        self.colors_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.colors_buttonBox.setObjectName("colors_buttonBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Colors"))
        self.label.setText(_translate("Dialog", "Time"))
        self.label_2.setText(_translate("Dialog", "Username"))
        self.label_3.setText(_translate("Dialog", "Message"))
        self.label_4.setText(_translate("Dialog", "Background"))

