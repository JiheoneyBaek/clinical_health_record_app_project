from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import login

class MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        uic.loadUi('start.ui', self)
        self.login = LoginPage()
        self.btnstart.clicked.connect(lambda: self.login_page_window())
    def login_page_window(self):
        self.close()
        self.login.show()

class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        uic.loadUi('login.ui', self)
        self.landing = LandingUI()
        self.btnlogin.clicked.connect(lambda: login.login_user(self))
    def landing_page_window(self):
        self.close()
        self.landing.show()

class LandingUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(LandingUI, self).__init__()
        uic.loadUi('landing.ui', self)

app = QtWidgets.QApplication(sys.argv)
window = MainWindows()
window.show()
app.exec_()