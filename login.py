import sys
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QTableWidget, QTableWidgetItem, QScroller, QAbstractItemView, QLineEdit
from PyQt5.QtGui import QIcon

# pyuic5 design code for UI
from login_design import Ui_MainWindow

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# from sqlalchemy model created
from model import Base, User
from client import client_ui


#==============DB integration =================
engine = create_engine('sqlite:///app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# context manager for updating the database
@contextmanager
def session_update():
    """Provide a transactional scope around a series of operations."""
    session = DBSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# context manager for querying the database
@contextmanager
def session_query():
    """Provide a transactional scope around a series of operations."""
    session = DBSession()
    yield session
    session.close()
#=========================================


class user_interface(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__() # this runs Qmainwindows __init__ method

        # setup the user interface from Designer
        self.setupUi(self)


        # if new user: then redirect
        self.actionRegister.triggered.connect(self.show_registration)

        self.menuLogin.menuAction().setVisible(False)
        #if accentally on register page get back to login page
        self.actionLogin_Page.triggered.connect(self.login_page)

        # all three signals mean that the user wants to login
        self.signInButton.clicked.connect(self.signIn)
        self.username_lineEdit.returnPressed.connect(self.signIn)
        self.password_lineEdit.returnPressed.connect(self.signIn)

        # action to make show password. Adds eye icon to password_lineEdit
        self.show_password = self.password_lineEdit.addAction(QIcon('icons/show.png'), QLineEdit.TrailingPosition)
        self.show_password.triggered.connect(self.show_password_action)
        # show password for registration page
        self.show_registration_password = self.register_password_lineEdit.addAction(QIcon('icons/show.png'), QLineEdit.TrailingPosition)
        self.show_registration_confirm_password = self.register_confirmPassword_lineEdit.addAction(QIcon('icons/show.png'), QLineEdit.TrailingPosition)
        self.show_registration_password.triggered.connect(self.show_registration_password_action)
        self.show_registration_confirm_password.triggered.connect(self.show_registration_confirm_password_action)

        # register button
        self.registerButton.clicked.connect(self.register)


        # show that the two password fields match or not
        self.register_confirmPassword_lineEdit.textChanged.connect(self.confirm_password_logo)
        self.register_password_lineEdit.textChanged.connect(self.confirm_password_logo)
        self.register_password_lineEdit.textChanged.connect(self.password_length_check)

    def password_length_check(self, password):
        for i in self.register_password_lineEdit.actions(): # returns a list of the actions
            if i is self.show_registration_password:
                continue
            else:
                self.register_password_lineEdit.removeAction(i)
        if len(password) < 6:
            red_x = self.register_password_lineEdit.addAction(QIcon('icons/red_x.png'), QLineEdit.TrailingPosition)
        else:
            green_x = self.register_password_lineEdit.addAction(QIcon('icons/checkmark.png'), QLineEdit.TrailingPosition)


    # QIcon for showing if the confirmation password is correct or not
    def confirm_password_logo(self, password):
        # this function is mapped to both changes in register_confirmPassword_lineEdit and register_password_lineEdit
        confirm_password = self.register_confirmPassword_lineEdit.text()
        for i in self.register_confirmPassword_lineEdit.actions(): # returns a list of the actions
            if i is self.show_registration_confirm_password:
                continue
            else:
                self.register_confirmPassword_lineEdit.removeAction(i)

        if confirm_password == '':
            pass
        elif confirm_password == self.register_password_lineEdit.text():
            green_x = self.register_confirmPassword_lineEdit.addAction(QIcon('icons/checkmark.png'), QLineEdit.TrailingPosition)
        else:
            red_x = self.register_confirmPassword_lineEdit.addAction(QIcon('icons/red_x.png'), QLineEdit.TrailingPosition)


    # code for registering a user into the database
    def register(self):
        if self.register_username_lineEdit.text() == '': # if empty
            self.register_message.setText("All fields must be filled")
        elif self.register_name_lineEdit.text() == '':
            self.register_message.setText("All fields must be filled")
        elif self.register_password_lineEdit.text() == '': # if empty
            self.register_message.setText("All fields must be filled")
        elif self.register_confirmPassword_lineEdit.text() == '': # if empty
            self.register_message.setText("All fields must be filled")
        elif len(self.register_password_lineEdit.text()) < 6:
            self.register_message.setText("Password is not long enough")
        else:
            password = self.register_password_lineEdit.text()
            confirm_password = self.register_confirmPassword_lineEdit.text()
            username = self.register_username_lineEdit.text()
            name = self.register_name_lineEdit.text()

            # connecting to the database
            with session_query() as session:
                user = session.query(User).filter(User.username == username).first()

            if user: # if user already exists
                self.register_message.setText("Username Already Exists")
            else: # user doesn't exist and can be created
                # need to make sure that the two passwords are the same
                if password != confirm_password:
                    self.register_message.setText("Passwords do not match")

                else: # passwords do match and we can commit to database
                    with session_update() as session:
                        new_user = User(username=username, name=name)
                        new_user.set_password(password)
                        session.add(new_user)
                        # context manager handles the commits and rollbacks and closes
                    self.register_message.setText("Registration Successful")

                    # now take it to the next page
                    #self.hide()




    # shows registration page after clicking in the QMenuBar
    def show_registration(self):
        # want to make the login action available incase user wants to get back to login page
        self.menuLogin.menuAction().setVisible(True)
        self.menuNew_User.menuAction().setVisible(False)
        self.stackedWidget.setCurrentIndex(1)

        # whatever message was left on login page we want to erase for when we go back
        self.login_feedback_label.clear()


    # shows the login page after going to registration page
    def login_page(self):
        self.menuNew_User.menuAction().setVisible(True)
        self.menuLogin.menuAction().setVisible(False)

        self.stackedWidget.setCurrentIndex(0)

    # sign In class method
    def signIn(self):
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        if username and password: # if there is text in

            # connecting to the database" using context managerd
            with session_query() as session:
                user = session.query(User).filter(User.username == username).first()

            if user: # then there was a match now check the password
                if user.check_password(password): # returns true if pw is correct
                    self.login_feedback_label.setText("Login Successful")
                    self.username_lineEdit.clear()
                    self.password_lineEdit.clear()


                    ### this will hide the current window but will not close program
                    ### could be useful for opening new window for program
                    self.hide()
                    # connecting to the messenger part of the app
                    self.messenger = client_ui(username)
                    self.messenger.show()

                else:
                    self.login_feedback_label.setText("Invalid Login. Try Again")
                    self.username_lineEdit.clear()
                    self.password_lineEdit.clear()
            else:
                self.login_feedback_label.setText("Invalid Login. Try Again")
                self.username_lineEdit.clear()
                self.password_lineEdit.clear()

        else: # one or both of the input is missing
            self.login_feedback_label.setText("Invalid Login. Try Again")
            self.username_lineEdit.clear()
            self.password_lineEdit.clear()

    # click on the icon and the password will show up as plain text to easily read
    def show_password_action(self):
        if self.password_lineEdit.echoMode() == 2:
            self.password_lineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_lineEdit.setEchoMode(QLineEdit.Password)

    # show passwords for the registration page
    def show_registration_password_action(self):
        if self.register_password_lineEdit.echoMode() == 2: # then it's in password mode
            self.register_password_lineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.register_password_lineEdit.setEchoMode(QLineEdit.Password)

    def show_registration_confirm_password_action(self):
        if self.register_confirmPassword_lineEdit.echoMode() == 2: # then it's in password mode
            self.register_confirmPassword_lineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.register_confirmPassword_lineEdit.setEchoMode(QLineEdit.Password)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = user_interface()
    window.show()
    sys.exit(app.exec_())
