from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3

table_header = ["UID", "Date/Time/", "Last Name", "First Name", "Middle Name", "Age","Birthday", "Sex", "Parent/Guardian", "Contact #"]
def SetupTable(self):
    self.tblPatients.clear()
    self.tblPatients.setRowCount(2)
    self.tblPatients.setColumnCount(10)
    for name in range(len(table_header)):
        self.tblPatients.setItem(0, name, QtWidgets.QTableWidgetItem(table_header[name]))
    self.tblPatients.verticalHeader().setVisible(False)
    self.tblPatients.setVisible(True)
    self.tblPatients.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.tblPatients.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    self.tblPatients.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

def tableShow(self):
    con = sqlite3.connect('db/clinical_health_app.db')
    cur = con.cursor()
    query = "SELECT * FROM patients"
    cur.execute(query)
    con.commit()
    records = cur.fetchall()
    print("success")
    for i in range(len(records)):
            currentRowCount = self.tblPatients.rowCount()-1
            self.tblPatients.insertRow(currentRowCount)
            for item in range(len(records[i])):
                self.tblPatients.setItem(currentRowCount, item, QtWidgets.QTableWidgetItem(str(records[i][item])))
    print(records)