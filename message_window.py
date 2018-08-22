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
        Form.resize(721, 538)
        font = QtGui.QFont()
        font.setFamily("Mitra Mono")
        Form.setFont(font)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 711, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.message_view = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(11)
        self.message_view.setFont(font)
        self.message_view.setFrameShape(QtWidgets.QFrame.Box)
        self.message_view.setReadOnly(True)
        self.message_view.setObjectName("message_view")
        self.verticalLayout.addWidget(self.message_view)
        self.message_textEdit = qChatEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.message_textEdit.setFont(font)
        self.message_textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.message_textEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.message_textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.message_textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message_textEdit.setObjectName("message_textEdit")
        self.verticalLayout.addWidget(self.message_textEdit)
        self.verticalLayout.setStretch(1, 8)
        self.verticalLayout.setStretch(2, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.name_label.setText(_translate("Form", "name_label"))
        self.message_view.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu Mono\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:9pt;\"><br /></p></body></html>"))
        self.message_textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu Mono\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:10pt;\"><br /></p></body></html>"))
        self.message_textEdit.setPlaceholderText(_translate("Form", "Insert Message Here"))

from mycomponent.qChatEdit import qChatEdit
