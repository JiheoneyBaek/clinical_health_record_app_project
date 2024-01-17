from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImageReader
import sqlite3
import traceback
import pandas as pd
import os
import csv
from pyreportjasper import PyReportJasper
import datetime
import getpass

con = sqlite3.connect("db\\clinical_health_app.db")
cur = con.cursor()
userfolder = getpass.getuser()


class MainWindows(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()
        uic.loadUi('start.ui', self)
        
        logdesc = "Session Started"
        createlog(logdesc)

        self.btnstart.clicked.connect(lambda: self.login_page_window())


    def login_page_window(self):
        self.hide()
        login.show()

    def closeEvent(self, event):
        dialog = QMessageBox.question(self, 'Exit?', f'Do you want to exit?', QMessageBox.Ok | QMessageBox.Cancel)
        if dialog == QMessageBox.Ok:
            dlg = QMessageBox(self)
            dlg.setIcon(QMessageBox.NoIcon)
            dlg.setWindowTitle("Thank you!")
            dlg.setText("Thank you for testing our app. -Carl&Jireh")
            button = dlg.exec()
            if button == QMessageBox.Ok:

                logdesc = "Session Stopped"
                createlog(logdesc)
                
                event.accept()
        else:
            event.ignore()
    def createlog(desc):
        x = datetime.datetime.now()
        logdatetime = x.strftime("%b"+" "+"%d"+", "+"%Y"+" | "+"%X")
        logquery = "INSERT INTO logs(DATETIME, DESCRIPTION) VALUES('"+logdatetime+"', '"+desc+"')"
        cur.execute(logquery)
        con.commit()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    style = """
            QWidget{
                background: #f2f2d2;
            }
            QLineEdit, QComboBox, QDateEdit, QDateTimeEdit, QPlainTextEdit{
                background: #fff;
                border-radius: 5px;
                padding: 3px;
            }
            QLabel{
                padding: 0px;
            }
            QPushButton{
                border-radius: 5px;
                background: green;
                border: 1px #DADADA solid;
                padding: 5px 2px;
                font-weight: bold;
                font-size: 9pt;
                outline: none;
                color: white;
            }
            #tblPatients, #tblLog{
                background: #fff;
                border: 1px #DADADA solid;
                border-radius: 10px;
            }
            QHeaderView, QHeaderView::section {
                background-color: burlywood;
            }
            QTableView::item:selected{
                background: #ffffde;
                color: black;
                font-weight: 500;
            }
            #btnADD, #btnImport, #btnSignup, #btnCreate{
                background: blue;
                color: white;
            }
            #btnEDIT, #btnExport, #btnlogin{
                background: green;
                color: white;
            }
            #btnDELETE, #btnDELALL, #btnCancel{
                background: red;
                color: white;
            }
            #btnPRINT, #btnForgot{
                background: orange;
                color: white;
            }
            #btnCLEAR{
                background: DarkMagenta;
                color: white;
            }
            #btnLogout{
                background: Maroon;
                color: white;
            }
            #btnLogs{
                background: MidnightBlue;
                color: white;
            }
            """
    app.setStyleSheet(style)
    window = MainWindows()
    login = LoginPage()
    landing = LandingUI()
    window.show()
    sys.exit(app.exec_())