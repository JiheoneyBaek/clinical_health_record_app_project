from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3

def signUp(self):
    name = self.txtName.text()
    username = self.txtUser.text()
    passkey = self.txtPass.text()
    try:
        if len(username) == 0 or len(passkey) == 0 or len(name) == 0:
            self.errorlog.setText("Please input all fields")
        else:
            dialog = QMessageBox.question(self, 'Create Account?', f'Are you sure you want to create an account?', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                sqliteConnection = sqlite3.connect("db\clinical_health_app.db")
                cursor = sqliteConnection.cursor()
                query = "INSERT INTO user (name, username, password) VALUES ('{name}', '{username}', '{passkey}')"
                cursor.execute(query)
            else:
                print("error")
            cursor.close()
            s
    except:
        print("Error")     