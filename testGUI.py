from mainGUI import Ui_test
import map
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QHeaderView,
    QApplication,
    QMainWindow,
    QDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)

import addsensor

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_test()
        self.ui.setupUi(self)
        self.ui.add_sens_pushButton.clicked.connect(self.add_sens)
        self.ui.show_sens_pushButton.clicked.connect(self.showtable)
        self.ui.add_db_date_pushButton.clicked.connect(self.showmap)

    
    def showtable(self):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT sensors.name, sensors.serial_number, type_sensors.type, sensors.N_S, sensors.E_W, sensors.installation_date, sensors.location
            FROM sensors
            JOIN type_sensors ON sensors.uid_type = type_sensors.uid_type;
            """
        )
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Название', 'Серийный номер', 'Тип', 'N/S', 'E/W', 'Дата установки', 'Местоположение'])
        while Query.next():
            rows = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.setRowCount(rows + 1)
            i = 0
            for i in range(7):
                self.ui.tableWidget.setItem(rows, i, QTableWidgetItem(str(Query.value(i))))
        
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(0)

    def coords_sens(self):
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT name, N_S, E_W, location FROM sensors
            """
        )
        
        coords = []
        while Query.next():
            tempcoords = []
            tempcoords.append(Query.value(0))
            tempcoords.append(Query.value(1))
            tempcoords.append(Query.value(2))
            tempcoords.append(Query.value(3))
            coords.append(tempcoords)
        
        return coords

    def showmap(self):
        new_map = map.Map(coords =  self.coords_sens())
        new_map.exec_()

    def add_sens(self):
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT * FROM type_sensors
            """
        )

        ls = {}
        while Query.next():
            ls[Query.value(0)] = Query.value(1)


        coords = self.coords_sens()

        new_sens = addsensor.AddSensor(self, ls=ls, coords=coords)
        new_sens.exec_()
        try:
            self.savesens(new_sens.saveValue())
        except:
            pass


    def savesens(self, ls):
        try:
            Query = QSqlQuery()
            Query.exec(
                f"""
                INSERT INTO sensors (name, serial_number, uid_type, N_S, E_W, installation_date, location)
                VALUES ('{ls[0]}', {ls[1]}, {ls[2]}, {ls[3]}, {ls[4]}, '{ls[5]}', '{ls[6]}') 
                """
            )
        except:
            pass




def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("contacts.sqlite")

    if not con.open():
        print("Database Error: %s" % con.lastError().databaseText())
        return False
    return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    if not createConnection():
        sys.exit(1)
    application = Application()
    application.show()
    sys.exit(app.exec_())