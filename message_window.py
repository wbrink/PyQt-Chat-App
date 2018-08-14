# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(499, 434)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 491, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.message_view = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.message_view.setFrameShape(QtWidgets.QFrame.Box)
        self.message_view.setReadOnly(True)
        self.message_view.setObjectName("message_view")
        self.verticalLayout.addWidget(self.message_view)
        self.message_textEdit = qChatEdit(self.verticalLayoutWidget)
        self.message_textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.message_textEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.message_textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.message_textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message_textEdit.setObjectName("message_textEdit")
        self.verticalLayout.addWidget(self.message_textEdit)
        self.verticalLayout.setStretch(1, 5)
        self.verticalLayout.setStretch(2, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name_label.setText(_translate("Form", "name_label"))
        self.message_textEdit.setPlaceholderText(_translate("Form", "Insert Message Here"))

from mycomponent.qChatEdit import qChatEdit

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

