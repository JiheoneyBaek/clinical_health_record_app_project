from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
import traceback
import pandas as pd
import os
import csv
import json
import pyreportjasper
from pyreportjasper import PyReportJasper

con = sqlite3.connect("db\\clinical_health_app.db")
cur = con.cursor()

class MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        uic.loadUi('start.ui', self)
        self.login = LoginPage()
        self.btnstart.clicked.connect(lambda: self.login_page_window())
    def login_page_window(self):
        self.hide()
        self.login.show()
    def closeEvent(self, event):
        dialog = QMessageBox.question(self, 'Exit?', f'Do you want to exit?', QMessageBox.Ok | QMessageBox.Cancel)
        if dialog == QMessageBox.Ok:
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.NoIcon)
            dlg.setWindowTitle("Thank you!")
            dlg.setText("Thank you for testing our app. -Carl&Jireh")
            button = dlg.exec()
            if button == QMessageBox.Ok:
                event.accept()
        else:
            event.ignore()

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
                dlg = QMessageBox(self)
                dlg.setIcon(QMessageBox.Critical)
                dlg.setWindowTitle("Error")
                dlg.setText("Please input all fields.")
                button = dlg.exec()
                if button == QMessageBox.Ok:
                    pass
            else:
                try:
                    query = 'SELECT username FROM account WHERE password =\''+passkey+"\'"
                    cur.execute(query)
                    result_pass = cur.fetchone()[0]
                    if result_pass == username:
                        dlg = QMessageBox(self)
                        dlg.setIcon(QMessageBox.Information)
                        dlg.setText("Welcome!")
                        button = dlg.exec()
                        if button == QMessageBox.Ok:
                            LandingUI.landing_page_window(self)
                    else:
                        pass
                except:
                    dlg1 = QMessageBox(self)
                    dlg1.setIcon(QMessageBox.Critical)
                    dlg1.setWindowTitle("Error")
                    dlg1.setText("Incorrect Username or Password. Please Try Again.")
                    dlg1.exec()

        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

            
    def back_to_main_window(self):
        self.hide()
        window.show()
        
class SignupUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignupUI, self).__init__()
        uic.loadUi('signup.ui', self)
        self.btnCreate.clicked.connect(lambda: self.signUp())
    def signup_page_window(self):
        dialog = QMessageBox.question(self, 'Create Account?', f'Do you want to create an account?', QMessageBox.Ok | QMessageBox.Cancel)
        if dialog == QMessageBox.Ok:
            self.hide()
            self.signup.show() 
        elif dialog == QMessageBox.Cancel:
            pass
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
        self.btnEDIT.clicked.connect(lambda: self.EditPatient())
        self.btnDELETE.clicked.connect(lambda: self.DeletePatient())
        # self.btnLogout.clicked.connect(lambda: self.Logout())
        self.btnExport.clicked.connect(lambda: self.ExportCSV())
        self.btnImport.clicked.connect(lambda: self.ImportCSV())
        self.btnDELALL.clicked.connect(lambda: self.DeleteAll())
        self.btnPRINT.clicked.connect(lambda: self.PrintPatientReport())
        self.tblPatients.clicked.connect(self.tableToLine)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.dateDT.setDateTime(QDateTime.currentDateTime()))
        self.timer.start(1000)
        
        self.chkLock.stateChanged.connect(self.lockPatient)
        self.chkLock.setChecked(0)

    def landing_page_window(self):
        self.hide()
        self.landing.show()

    def setupTable(self):
        query = "SELECT * FROM patients"
        cur.execute(query)
        table_header = list(map(lambda x: x[0], cur.description))
        self.tblPatients.clear()
        self.tblPatients.setRowCount(0)
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
            currentRowCount = self.tblPatients.rowCount()
            self.tblPatients.insertRow(currentRowCount)
            for item in range(len(records[i])):
                self.tblPatients.setItem(currentRowCount, item, QtWidgets.QTableWidgetItem(str(records[i][item])))

    def tableToLine(self):
        try:
            index=(self.tblPatients.selectionModel().currentIndex())
            value= index.siblingAtColumn(0).data()
            query = 'SELECT * from patients WHERE UID=\''+value+"\'"
            cur.execute(query)
            patientInfo = list(cur.fetchone())

            uid = str(patientInfo[0])
            lastname = patientInfo[1]
            firstname = patientInfo[2]
            middlename = patientInfo[3]
            age = str(patientInfo[4])
            address = patientInfo[6]
            birthday = str(patientInfo[7])
            sex = str(patientInfo[8])
            guardian = patientInfo[9]
            contactnum = str(patientInfo[10])
            doctor = patientInfo[11]
            doctorsnote = patientInfo[12]
            bp = str(patientInfo[13])
            rr = str(patientInfo[14])
            hr = str(patientInfo[15])
            wt = str(patientInfo[16])
            temp = str(patientInfo[17])
            
            formattedbd = QtCore.QDate.fromString(birthday, "yyyy-MM-dd")
            
            self.txtUID.setText(uid)
            self.txtLname.setText(lastname)
            self.txtFname.setText(firstname)
            self.txtMname.setText(middlename)
            self.txtAdd.setText(address)
            self.txtAge.setText(age)
            self.txtGuardian.setText(guardian)
            self.cbxSex.setCurrentText(sex)
            self.dateBirth.setDate(formattedbd)
            self.txtDoctor.setText(doctor)
            self.txtContact.setText(contactnum)
            self.txtNotes.setPlainText(doctorsnote)
            self.txtBP.setText(bp)
            self.txtHR.setText(hr)
            self.txtRR.setText(rr)
            self.txtWT.setText(wt)
            self.txtTemp.setText(temp)
            
            self.chkLock.setChecked(1)

        except TypeError:
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.Critical)
            dlg.setWindowTitle("Error")
            dlg.setText("An Error Occurred!")
            button = dlg.exec()
            if button == QMessageBox.Ok:
                pass
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

        
        
        try:
            dialog = QMessageBox.question(self, 'Add Patient?', f'Are you sure you want to add a patient info?', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                query = "INSERT INTO patients(LNAME, FNAME, MNAME, AGE, ADDRESS, SEX, GUARDIAN, CONTACTNUM, DOCTOR, BP, HR, RR, WT, TEMP, BIRTHDAY, DATETIME, DOCTORSNOTE) VALUES('"+lname+"', '"+fname+"', '"+mname+"', '"+age+"', '"+address+"', '"+sex+"', '"+parent+"', '"+contact+"','"+doc+"', '"+bp+"', '"+hr+"', '"+rr+"', '"+wt+"', '"+temp+"', '"+birthday+"', '"+datetime+"','"+note+"')"
                cur.execute(query)
                con.commit()
                self.setupTable()
                self.showTable()
                dlg = QMessageBox(self)
                dlg.setIcon(QMessageBox.Information)
                dlg.setWindowTitle("Success")
                dlg.setText("Patient added successfully!")
                button = dlg.exec()
                if button == QMessageBox.Ok:
                    pass
                self.chkLock.setChecked(1)
            else:
                dlg1 = QMessageBox(self)
                dlg1.setIcon(QMessageBox.Information)
                dlg1.setWindowTitle("Success")
                dlg1.setText("User cancelled the operation.")
                button1 = dlg1.exec()
                if button1 == QMessageBox.Ok:
                    pass
        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def EditPatient(self):
        uid = self.txtUID.text()
        lname = self.txtLname.text()
        fname = self.txtFname.text()
        mname = self.txtMname.text()
        address = self.txtAdd.text()
        age = self.txtAge.text()
        parent = self.txtGuardian.text()
        sex = self.cbxSex.currentText()
        birthday = str(self.dateBirth.date().toString("yyyy-MM-dd"))
        doc = self.txtDoctor.text()
        contact = self.txtContact.text()
        note  = self.txtNotes.toPlainText()
        bp = self.txtBP.text()
        hr = self.txtHR.text()
        rr = self.txtRR.text()
        wt = self.txtWT.text()
        temp = self.txtTemp.text()

        try:
            dialog = QMessageBox.question(self, 'Edit Patient?', f'Are you sure you want to edit patient info?', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                query = "UPDATE patients SET LNAME = '"+lname+"', FNAME = '"+fname+"', MNAME = '"+mname+"', AGE = '"+age+"', ADDRESS = '"+address+"', SEX = '"+sex+"', GUARDIAN = '"+parent+"', CONTACTNUM = '"+contact+"', DOCTOR = '"+doc+"', BP = '"+bp+"', HR = '"+hr+"', RR = '"+rr+"', WT = '"+wt+"', TEMP = '"+temp+"', BIRTHDAY = '"+birthday+"', DOCTORSNOTE = '"+note+"' WHERE UID = '"+uid+"'"
                cur.execute(query)
                con.commit()
                self.chkLock.setChecked(1)
                self.setupTable()
                self.showTable()
                dlg = QMessageBox(self)
                dlg.setIcon(QMessageBox.Information)
                dlg.setWindowTitle("Success")
                dlg.setText("Patient edited successfully!")
                button = dlg.exec()
                if button == QMessageBox.Ok:
                    pass
                self.chkLock.setChecked(1)
            else:
                dlg1 = QMessageBox(self)
                dlg1.setIcon(QMessageBox.Information)
                dlg1.setWindowTitle("Success")
                dlg1.setText("User cancelled the operation.")
                button1 = dlg1.exec()
                if button1 == QMessageBox.Ok:
                    pass
                
        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def DeletePatient(self):
        try:
            dialog = QMessageBox.question(self, 'Delete Patient?', f'Are you sure you want to delete patient? This is cannot be undone.', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                uid = self.txtUID.text()
                query = 'DELETE FROM patients where UID = \''+uid+"\'"
                cur.execute(query)
                con.commit()
                self.ClearPatient()
                self.setupTable()
                self.showTable()
                dlg = QMessageBox(self)
                dlg.setIcon(QMessageBox.Information)
                dlg.setWindowTitle("Success")
                dlg.setText("Patient's data successfully deleted!")
            else:
                dlg1 = QMessageBox(self)
                dlg1.setIcon(QMessageBox.Information)
                dlg1.setWindowTitle("Success")
                dlg1.setText("User cancelled the operation.")
                button1 = dlg1.exec()
                if button1 == QMessageBox.Ok:
                    pass

        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def lockPatient(self, checked):
        if checked:
            self.txtLname.setReadOnly(True)
            self.txtFname.setReadOnly(True)
            self.txtMname.setReadOnly(True)
            self.txtAdd.setReadOnly(True)
            self.txtAge.setReadOnly(True)
            self.txtGuardian.setReadOnly(True)
            self.dateBirth.setReadOnly(True)
            self.txtDoctor.setReadOnly(True)
            self.txtContact.setReadOnly(True)
            self.txtNotes.setReadOnly(True)
            self.txtBP.setReadOnly(True)
            self.txtHR.setReadOnly(True)
            self.txtRR.setReadOnly(True)
            self.txtWT.setReadOnly(True)
            self.txtTemp.setReadOnly(True)
        else: 
            self.txtLname.setReadOnly(False)
            self.txtFname.setReadOnly(False)
            self.txtMname.setReadOnly(False)
            self.txtAdd.setReadOnly(False)
            self.txtAge.setReadOnly(False)
            self.txtGuardian.setReadOnly(False)
            self.dateBirth.setReadOnly(False)
            self.txtDoctor.setReadOnly(False)
            self.txtContact.setReadOnly(False)
            self.txtNotes.setReadOnly(False)
            self.txtBP.setReadOnly(False)
            self.txtHR.setReadOnly(False)
            self.txtRR.setReadOnly(False)
            self.txtWT.setReadOnly(False)
            self.txtTemp.setReadOnly(False)
            dlg1 = QMessageBox(self)
            dlg1.setIcon(QMessageBox.Information)
            dlg1.setWindowTitle("Success")
            dlg1.setText("Editing is unlocked!")
            button1 = dlg1.exec()
            if button1 == QMessageBox.Ok:
                pass


    def ClearPatient(self):
        self.txtUID.clear()
        self.txtLname.clear()
        self.txtFname.clear()
        self.txtMname.clear()
        self.txtAdd.clear()
        self.txtAge.clear()
        self.txtGuardian.clear()
        self.cbxSex.currentText()
        self.txtDoctor.clear()
        self.txtContact.clear()
        self.txtNotes.clear()
        self.txtBP.clear()
        self.txtHR.clear()
        self.txtRR.clear()
        self.txtWT.clear()
        self.txtTemp.clear()
        
        formattedbd = QtCore.QDate.fromString("2000-01-01", "yyyy-MM-dd")
        self.dateBirth.setDate(formattedbd)
        self.chkLock.setChecked(0)

        self.setupTable()
        self.showTable()

    def ImportCSV(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
            self.all_data = pd.read_csv(path[0])
            str2 = str(path[0])

            with open(str2, newline = '') as f:
                reader = csv.reader(f)
                data = list(reader)

                i = 0
                while i < len(data):
                    query = "INSERT INTO patients(LNAME, FNAME, MNAME, AGE, DATETIME, ADDRESS, BIRTHDAY, SEX, GUARDIAN, CONTACTNUM, DOCTOR,  DOCTORSNOTE, BP, RR, HR, WT, TEMP) VALUES('"+data[i][1]+"', '"+data[i][2]+"', '"+data[i][3]+"', '"+data[i][4]+"', '"+data[i][5]+"', '"+data[i][6]+"', '"+data[i][7]+"', '"+data[i][8]+"','"+data[i][9]+"', '"+data[i][10]+"', '"+data[i][11]+"', '"+data[i][12]+"', '"+data[i][13]+"', '"+data[i][14]+"', '"+data[i][15]+"', '"+data[i][16]+"','"+data[i][17]+"')"
                    cur.execute(query)
                    con.commit()
                    i+=1
            self.setupTable()
            self.showTable()
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.Information)
            dlg.setWindowTitle("Success")
            dlg.setText("Patient added successfully!")
            dlg.exec()

        except FileNotFoundError:
            dlg1 = QMessageBox(self)
            dlg1.setIcon(QMessageBox.Information)
            dlg1.setWindowTitle("Success")
            dlg1.setText("User cancelled the operation.")
            dlg1.exec()

    def DeleteAll(self):
        try:
            dialog = QMessageBox.question(self, 'Delete All Patient?', f'Are you sure you want to delete all patients? This is cannot be undone.', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                query = "DELETE FROM patients"
                cur.execute(query)
                con.commit()
                self.ClearPatient()
                self.setupTable()
                self.showTable()
                dlg = QMessageBox(self)
                dlg.setIcon(QMessageBox.Information)
                dlg.setWindowTitle("Success")
                dlg.setText("All data are successfully deleted!")
                dlg.exec()
            else:
                dlg1 = QMessageBox(self)
                dlg1.setIcon(QMessageBox.Information)
                dlg1.setWindowTitle("Success")
                dlg1.setText("User cancelled the operation.")
                button1 = dlg1.exec()
                if button1 == QMessageBox.Ok:
                    pass
        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def ExportCSV(self):
        try:
            datetime = str(self.dateDT.dateTime().toString("yyyy-MM-dd"))
            dialog = QMessageBox.question(self, 'Export to CSV?', f'Are you sure you want to export to CSV?', QMessageBox.Ok | QMessageBox.Cancel)
            if dialog == QMessageBox.Ok:
                path = datetime + " Patients.csv"
                df = pd.read_sql('SELECT * from patients', con)
                df.to_csv(path, index = False)
                dlg = QMessageBox(self)
                dlg.setIcon(QMessageBox.Information)
                dlg.setWindowTitle("Success")
                dlg.setText("Successfully Exported")
                dlg.exec()
            else:
                dlg1 = QMessageBox(self)
                dlg1.setIcon(QMessageBox.Information)
                dlg1.setWindowTitle("Success")
                dlg1.setText("User cancelled the operation.")
                dlg1.exec()
        except sqlite3.Error as er:
            print("error")
            print('SQLite error: %s' % (' '.join(er.args)))
            print("Exception class is: ", er.__class__)
            print('SQLite traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    # def PrintPatientReport(self):

    #     lname = self.txtLname.text()
    #     fname = self.txtFname.text()
    #     mname = self.txtMname.text()
    #     address = self.txtAdd.text()
    #     age = self.txtAge.text()
    #     parent = self.txtGuardian.text()
    #     sex = self.cbxSex.currentText()
    #     birthday = str(self.dateBirth.date().toString("yyyy-MM-dd"))
    #     datetime = str(self.dateDT.dateTime().toString("yyyy-MM-dd hh:mm"))
    #     doc = self.txtDoctor.text()
    #     contact = self.txtContact.text()
    #     note  = self.txtNotes.toPlainText()
    #     bp = self.txtBP.text()
    #     hr = self.txtHR.text()
    #     rr = self.txtRR.text()
    #     wt = self.txtWT.text()
    #     temp = self.txtTemp.text()

    #     aDict = {"lname":lname, "fname":fname, "mname":mname, "address":address, "age":age, "sex":sex, "dt":datetime, "bd":birthday, "parent":parent, "contactnum":contact, "doc":doc, "note":note, "bp":bp, "hr":hr, "wt":wt, "rr":rr, "temp":temp,}
    #     jsonString = json.dumps(aDict)
    #     jsonFile = open("data.json", "w")
    #     jsonFile.write(jsonString)
    #     jsonFile.close()

    #     try:
    #         RESOURCES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'resources')
    #         REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
    #         input_file = os.path.join(REPORTS_DIR, 'patientreport.jrxml')
    #         output_file = os.path.join(REPORTS_DIR, 'json')
    #         conn = {
    #             'driver': 'json',
    #             'data_file': os.path.join(self.RESOURCES_DIR, 'data.json'),
    #             'json_query': 'contacts.person'
    #         }
    #         pyreportjasper = PyReportJasper()
    #         self.pyreportjasper.config(
    #             input_file,
    #             output_file,
    #             output_formats=["pdf"],
    #             db_connection=conn
    #         )
    #         self.pyreportjasper.process_report()
    #         print('Result is the file below.')
    #         print(output_file + '.pdf')
    #     except:
    #         pass
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindows()
    window.show()
    sys.exit(app.exec_())
