from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
import signup

def login_user(self):
    username = self.txtUser.text()
    passkey = self.txtPass.text()
    self.landing = LandingUI()
    
    try:
        if len(username) == 0 or len(passkey) == 0:
            self.errorlog.setText("Please input all fields")
        else:
            sqliteConnection = sqlite3.connect("db\\clinical_health_app.db")
            cursor = sqliteConnection.cursor()
            query = 'SELECT password FROM account WHERE username =\''+username+"\'"
            cursor.execute(query)
            result_pass = cursor.fetchone()[0]
            if result_pass == passkey:
                self.errorlog.setText("Success")
                LandingUI.landing_page_window(self)
            else:
                self.errorlog.setText("Incorrect Username or Password")
            cursor.close()
    except:
        print("Error")

def createButton(self):
    dialog = QMessageBox.question(self, 'Create Account?', f'Do you want to create an account?', QMessageBox.Ok | QMessageBox.Cancel)
    if dialog == QMessageBox.Ok:
        SignupUI.signup_page_window(self)  
    elif dialog == QMessageBox.Cancel:
        self.close()              

class LandingUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(LandingUI, self).__init__()
        uic.loadUi('landing.ui', self)
    def landing_page_window(self):
        self.close()
        self.landing.show()

class SignupUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignupUI, self).__init__()
        uic.loadUi('signup.ui', self)
        self.btnCreate.clicked.connect(lambda: signup.signUp(self))
    def signup_page_window(self):
        dialog = QMessageBox.question(self, 'Create Account?', f'Do you want to create an account?', QMessageBox.Ok | QMessageBox.Cancel)
        if dialog == QMessageBox.Ok:
            self.signup.show()
            self.close()     
        elif dialog == QMessageBox.Cancel:
            self.close()              