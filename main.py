from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
import traceback

con = sqlite3.connect("db\\clinical_health_app.db")
cur = con.cursor()

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
                query = 'SELECT username FROM account WHERE password =\''+passkey+"\'"
                cur.execute(query)
                result_pass = cur.fetchone()[0]
                if result_pass == username:
                    self.errorlog.setText("Success")
                    LandingUI.landing_page_window(self)
                else:
                    self.errorlog.setText("Incorrect Username or Password")

        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
            
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
                    query = "INSERT INTO account(username, password, name) VALUES('"+username+"', '"+passkey+"', '"+name+"')"
                    cur.execute(query)
                    con.commit()
                    print("success")
        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

class LandingUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(LandingUI, self).__init__()
        uic.loadUi('landing.ui', self)
        self.setupTable()
        self.showTable()
        self.btnADD.clicked.connect(lambda: self.AddPatient())
        self.btnCLEAR.clicked.connect(lambda: self.ClearPatient())
    def landing_page_window(self):
        self.close()
        self.landing.show()
    def setupTable(self):
        query = "SELECT * FROM patients"
        cur.execute(query)
        table_header = list(map(lambda x: x[0], cur.description))
        self.tblPatients.clear()
        self.tblPatients.setRowCount(1)
        self.tblPatients.setColumnCount(18)
        for name in range(len(table_header)):
            self.tblPatients.setHorizontalHeaderItem(name, QTableWidgetItem(table_header[name]))
            self.tblPatients.verticalHeader().setVisible(False)
            self.tblPatients.setVisible(True)
            self.tblPatients.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tblPatients.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tblPatients.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.tblPatients.setSelectionBehavior(QAbstractItemView.SelectRows)
    def showTable(self):
        cur.execute("SELECT * FROM patients")
        records = cur.fetchall()
        
        for i in range(len(records)):
            currentRowCount = self.tblPatients.rowCount()-1
            self.tblPatients.insertRow(currentRowCount)
            for item in range(len(records[i])):
                self.tblPatients.setItem(currentRowCount, item, QtWidgets.QTableWidgetItem(str(records[i][item])))
        print(records)

    def AddPatient(self):
        lname = self.txtLname.text()
        fname = self.txtFname.text()
        mname = self.txtMname.text()
        address = self.txtAdd.text()
        age = self.txtAge.text()
        parent = self.txtGuardian.text()
        sex = self.cbxSex.currentText()
        birthday = str(self.dateBirth.date().toString("yyyy-MM-dd"))
        datetime = str(self.dateDT.dateTime().toString("yyyy-MM-dd hh:mm"))
        doc = self.txtDoctor.text()
        contact = self.txtContact.text()
        note  = self.txtNotes.toPlainText()
        bp = self.txtBP.text()
        hr = self.txtHR.text()
        rr = self.txtRR.text()
        wt = self.txtWT.text()
        temp = self.txtTemp.text()

        query = "INSERT INTO patients(LNAME, FNAME, MNAME, AGE, ADDRESS, SEX, GUARDIAN, CONTACTNUM, DOCTOR, BP, HR, RR, WT, TEMP, BIRTHDAY, DATETIME, DOCTORSNOTE) VALUES('"+lname+"', '"+fname+"', '"+mname+"', '"+age+"', '"+address+"', '"+sex+"', '"+parent+"', '"+contact+"','"+doc+"', '"+bp+"', '"+hr+"', '"+rr+"', '"+wt+"', '"+temp+"', '"+birthday+"', '"+datetime+"','"+note+"')"

        
        try:
            dialog = QMessageBox.question(self, 'Add Patient?', f'Are you sure you want to add a patient info?', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                cur.execute(query)
                con.commit()
                self.setupTable()
                self.showTable()
                print("success")
        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
    def ClearPatient(self):
        self.txtLname.clear()
        self.txtFname.clear()
        self.txtMname.clear()
        self.txtAdd.clear()
        self.txtAge.clear()
        self.txtGuardian.clear()
        self.cbxSex.currentText()
        # self.dateBirth.date().toString("yyyy-MM-dd"))
        # self.dateDT.dateTime().toString("yyyy-MM-dd hh:mm"))
        self.txtDoctor.clear()
        self.txtContact.clear()
        self.txtNotes.clear()
        self.txtBP.clear()
        self.txtHR.clear()
        self.txtRR.clear()
        self.txtWT.clear()
        self.txtTemp.clear()
app = QtWidgets.QApplication(sys.argv)
window = MainWindows()
window.show()
app.exec_()