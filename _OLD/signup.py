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
    print(name, username, passkey)
    try:
        if len(username) == 0 or len(passkey) == 0 or len(name) == 0:
            self.errorlog.setText("Please input all fields")
        else:
            dialog = QMessageBox.question(self, 'Create Account?', f'Are you sure you want to create an account?', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                con = sqlite3.connect('db/clinical_health_app.db')
                cur = con.cursor()
                query = "INSERT INTO account(username, password, name) VALUES('"+username+"', '"+passkey+"', '"+name+"')"
                cur.execute(query)
                con.commit()
                print("success")

    except:
        print("error")