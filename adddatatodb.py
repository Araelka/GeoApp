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
            self.ui.RH_comboBox.addItem(headers[i], i)
            self.ui.PAR_comboBox.addItem(headers[i], i)
            self.ui.rain_comboBox.addItem(headers[i], i)
            self.ui.current_comboBox.addItem(headers[i], i)
            self.ui.pressure_comboBox.addItem(headers[i], i)
            self.ui.gust_speed_comboBox.addItem(headers[i], i)
            self.ui.wind_speed_comboBox.addItem(headers[i], i)
            self.ui.solar_radiation_comboBox.addItem(headers[i], i)
            self.ui.wond_direction_comboBox.addItem(headers[i], i)
            self.ui.temp_ground_comboBox.addItem(headers[i], i)
        temt_type = ['°F', '°C']    
        for i in range(0,2):
            self.ui.tempC_air_comboBox.addItem(temt_type[i], i)
            self.ui.tempCF_ground_comboBox.addItem(temt_type[i], i)
            

        self.ui.add_date_to_db_pushButton.clicked.connect(self.adddatabutton)
        self.isClose = 0

    def adddatabutton(self):
        try:
            self.sensor = int(self.ui.sensor_comboBox.currentData())
        except:
            pass
        try:
            self.date = int(self.ui.date_comboBox.currentData())
        except:
            pass
        try:
            self.time = int(self.ui.time_comboBox.currentData())
        except:
            pass
        try:
            self.water_content = int(self.ui.water_content_comboBox.currentData())
        except:
            pass
        try:
            self.current = int(self.ui.current_comboBox.currentData())
        except:
            pass
        try:
            self.PAR = int(self.ui.PAR_comboBox.currentData())
        except:
            pass
        try:
            self.temp_air = int(self.ui.temp_air_comboBox.currentData())
            self.airtype = int(self.ui.tempC_air_comboBox.currentData())
        except:
            pass
        try:
            self.RH = int(self.ui.RH_comboBox.currentData())
        except:
            pass
        try:
            self.wind_speed = int(self.ui.wind_speed_comboBox.currentData())
        except:
            pass
        try:
            self.gust_speed = int(self.ui.gust_speed_comboBox.currentData())
        except:
            pass
        try:
            self.wind_direction = int(self.ui.wond_direction_comboBox.currentData())
        except:
            pass
        try:
            self.temp_ground = int(self.ui.temp_ground_comboBox.currentData())
            self.groundtype = int(self.ui.tempCF_ground_comboBox.currentData())
        except:
            pass
        try:
            self.pressure = int(self.ui.pressure_comboBox.currentData())
        except:
            pass
        try:
            self.rain = int(self.ui.rain_comboBox.currentData())
        except:
            pass
        try:
            self.solar_radiation = int(self.ui.solar_radiation_comboBox.currentData())
        except:
            pass

        self.isClose = 1    
        self.close()