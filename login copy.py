from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3


class loginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(loginPage, self).__init__()
        uic.loadUi("login.ui",self)
        self.landing = LandingUI()
        self.btnlogin.clicked.connect(lambda: self.login_user())
    def login_user(self):
        username = self.txtUser.text()
        password = self.txtPass.text()
        try:
            sqliteConnection = sqlite3.connect('db/clinical_health_app.db')
            cursor = sqliteConnection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE username=? and password=?")
            sqliteConnection.commit()
            cursor.close()
            self.close()
            self.landing.show()    
        except:
            print("Incorrect Username or Password")

class LandingUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(LandingUI, self).__init__()
        uic.loadUi('landing.ui', self)

app = QtWidgets.QApplication(sys.argv)
window = loginPage()
window.show()
app.exec_()