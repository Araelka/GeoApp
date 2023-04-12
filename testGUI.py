from GUI import Ui_test
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
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
        self.ui.pushButton_2.clicked.connect(self.add_sens)

    
    def showtable(self):
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT sensors.uid_sensor, type_sensors.type, sensors.location
            FROM sensors
            JOIN type_sensors ON sensors.uid_type = type_sensors.uid_type;
            """
        )

        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Id Датчика', 'Тип сенсора', 'Местоположение'])
        while Query.next():
            rows = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.setRowCount(rows + 1)
            i = 0
            for i in range(3):
                self.ui.tableWidget.setItem(rows, i, QTableWidgetItem(str(Query.value(i))))
            # self.ui.tableWidget.setItem(rows, 1, QTableWidgetItem(str(Query.value(1))))
            # self.ui.tableWidget.setItem(rows, 2, QTableWidgetItem(str(Query.value(2))))
            # self.ui.tableWidget.setItem(rows, 3, QTableWidgetItem(str(Query.value(3))))
        # self.ui.tableWidget.resizeColumnsToContents()
        # self.setCentralWidget(self.ui.tableWidget)

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

        Query.exec(
            """
            SELECT name, N_S, E_W FROM sensors
            """
        )
        
        coords = []
        while Query.next():
            tempcoords = []
            tempcoords.append(Query.value(0))
            tempcoords.append(Query.value(1))
            tempcoords.append(Query.value(2))
            coords.append(tempcoords)

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