import sys
from  GUIadddatetodb import Ui_add_date_to_db
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

class Adddatatodb(QDialog):
    def __init__(self, parent=None, sensors={}, headers={}):
        super(Adddatatodb, self).__init__(parent) 
        self.ui = Ui_add_date_to_db()
        self.ui.setupUi(self)
        for i in sensors:
            self.ui.sensor_comboBox.addItem(sensors[i], i)
        for i in headers:
            self.ui.date_comboBox.addItem(headers[i], i)
            self.ui.time_comboBox.addItem(headers[i], i)
            self.ui.water_content_comboBox.addItem(headers[i], i)
            self.ui.temp_air_comboBox.addItem(headers[i], i)
        self.ui.add_date_to_db_pushButton.clicked.connect(self.adddatabutton)

    def adddatabutton(self):
        try:
            self.sensor = int(self.ui.sensor_comboBox.currentData())
            self.date = int(self.ui.date_comboBox.currentData())
            self.time = int(self.ui.time_comboBox.currentData())
            self.tempair = int(self.ui.temp_air_comboBox.currentData())
            self.close()
        except:
            pass