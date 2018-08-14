from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal

class qChatEdit(QTextEdit):
    # define a new signal called returnPressed
    returnPressed = pyqtSignal()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            # emit the signal 
            self.returnPressed.emit()
        else:
            # call base class keyPressEvent
            QTextEdit.keyPressEvent(self, e)
