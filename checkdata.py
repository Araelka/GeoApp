import sys
from  GUIcheckdata import Ui_check_data_Dialog
import map
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QWidget,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

class DataCheck(QDialog):
    def __init__(self, parent=None):
        super(DataCheck, self).__init__(parent) 
        self.ui = Ui_check_data_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.check)
        self.ui.temp_min_textEdit.setText('-45')
        self.ui.temp_max_textEdit.setText('45')
        self.ui.rh_min_textEdit.setText('-100')
        self.ui.rh_max_textEdit.setText('100')

    def check(self):
        self.temp = []
        self.temp.append(float(self.ui.temp_min_textEdit.toPlainText()))
        self.temp.append(float(self.ui.temp_max_textEdit.toPlainText()))

        self.RH = []
        self.RH.append(float(self.ui.rh_min_textEdit.toPlainText()))
        self.RH.append(float(self.ui.rh_max_textEdit.toPlainText()))

        self.close()
        