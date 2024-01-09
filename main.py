from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3

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
        self.signup = SignupUI()
        self.landing = LandingUI()
        self.btnlogin.clicked.connect(lambda: self.login_user())
        self.btnSignup.clicked.connect(lambda: SignupUI.signup_page_window(self))
        self.btnCancel.clicked.connect(lambda: self.back_to_main_window())

    def login_user(self):
        username = self.txtUser.text()
        passkey = self.txtPass.text()
        try:
            if len(username) == 0 or len(passkey) == 0:
                self.errorlog.setText("Please input all fields")
            else:
                sqliteConnection = sqlite3.connect("db\\clinical_health_app.db")
                cursor = sqliteConnection.cursor()
                query = 'SELECT username FROM account WHERE password =\''+passkey+"\'"
                cursor.execute(query)
                result_pass = cursor.fetchone()[0]
                if result_pass == username:
                    self.errorlog.setText("Success")
                    LandingUI.landing_page_window(self)
                else:
                    self.errorlog.setText("Incorrect Username or Password")
                cursor.close()
        except:
            print("Error")
            
    def back_to_main_window(self):
        self.close()
        window.show()

class SignupUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignupUI, self).__init__()
        uic.loadUi('signup.ui', self)
        self.btnCreate.clicked.connect(lambda: self.signUp())
    def signup_page_window(self):
        dialog = QMessageBox.question(self, 'Create Account?', f'Do you want to create an account?', QMessageBox.Ok | QMessageBox.Cancel)
        if dialog == QMessageBox.Ok:
            self.close()
            self.signup.show() 
        elif dialog == QMessageBox.Cancel:
            self.close()
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

class LandingUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(LandingUI, self).__init__()
        uic.loadUi('landing.ui', self)
        # self.SetupTable(self)
        # self.tableShow(self)
    def landing_page_window(self):
        self.close()
        self.landing.show()
    # table_header = ["UID", "Date/Time/", "Last Name", "First Name", "Middle Name", "Age","Birthday", "Sex", "Parent/Guardian", "Contact #"]
    # def SetupTable(self):
    #     self.tblPatients.clear()
    #     self.tblPatients.setRowCount(2)
    #     self.tblPatients.setColumnCount(10)
    #     for name in range(len(table_header)):
    #         self.tblPatients.setItem(0, name, QtWidgets.QTableWidgetItem(table_header[name]))
    #     self.tblPatients.verticalHeader().setVisible(False)
    #     self.tblPatients.setVisible(True)
    #     self.tblPatients.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #     self.tblPatients.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    #     self.tblPatients.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    # def tableShow(self):
    #     con = sqlite3.connect('db/clinical_health_app.db')
    #     cur = con.cursor()
    #     query = "SELECT * FROM patients"
    #     cur.execute(query)
    #     con.commit()
    #     records = cur.fetchall()
    #     print("success")
    #     for i in range(len(records)):
    #             currentRowCount = self.tblPatients.rowCount()-1
    #             self.tblPatients.insertRow(currentRowCount)
    #             for item in range(len(records[i])):
    #                 self.tblPatients.setItem(currentRowCount, item, QtWidgets.QTableWidgetItem(str(records[i][item])))
    #     print(records)
app = QtWidgets.QApplication(sys.argv)
window = MainWindows()
window.show()
app.exec_()