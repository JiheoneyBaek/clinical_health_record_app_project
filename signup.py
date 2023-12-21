from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3

def signUp(self):
    name = self.txtName.text()
    username = self.txtUname.text()
    passkey = self.txtPass.text()
    try:
        if len(username) == 0 or len(passkey) == 0 or len(name) == 0:
            self.errorlog.setText("Please input all fields")
        else:
            sqliteConnection = sqlite3.connect("db\clinical_health_app.db")
            cursor = sqliteConnection.cursor()
            query = "INSERT INTO user (name, username, password) VALUES ('{name}', '{username}', '{passkey}')"
            cursor.execute(query)
            if result_pass == passkey:

                LandingUI.landing_page_window(self)
            else:
                self.errorlog.setText("Incorrect Username or Password")
            cursor.close()
    except:
        print("Error")     