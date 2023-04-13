from mainGUI import Ui_test
import map
import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QHeaderView,
    QApplication,
    QMainWindow,
    QDialog,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
import pandas as pd

import addsensor
import adddatatodb

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_test()
        self.ui.setupUi(self)
        self.ui.add_sens_pushButton.clicked.connect(self.add_sens)
        self.ui.show_sens_pushButton.clicked.connect(self.showtable)
        # self.ui.add_db_date_pushButton.clicked.connect(self.showmap)
        self.ui.add_date_pushButton.clicked.connect(self.uploadfile)
        self.ui.show_date_db_pushButton.clicked.connect(self.showalldb)
        self.ui.add_db_date_pushButton.clicked.connect(self.showadata)
    
    # Загрузка данных из в файла в dataframe
    def uploadfile(self):
        filename = QFileDialog.getOpenFileName(self, 'Открыть файл', '*.csv')
        
        if filename[0]:
            try:
                self.df = pd.read_csv(filename[0], skiprows = 1)
                self.df = self.df.loc[0:2]
            except:
                return 0
            self.df = self.df.drop(columns = self.df.columns[0])
            self.df[self.df.columns[0]] = pd.to_datetime(self.df[self.df.columns[0]])
            # Изменить формат даты и времени
            self.df.insert(0, 'Time, GMT+07:00', self.df['Date Time, GMT+07:00'].dt.time)
            self.df.insert(0, 'Date, GMT+07:00', self.df['Date Time, GMT+07:00'].dt.date)
            self.df = self.df.drop(columns=self.df.columns[2])
            self.showlastfile(self.df)

    # Отрисовка последнего или переданного datafrema
    def showlastfile(self, df):
        try:
            if df==False:
                try:
                    df = self.df
                except:
                    pass
        except:
            pass

        try:
            self.ui.tableWidget.setColumnCount(len(df.columns))
            self.ui.tableWidget.setRowCount(len(df.index))
            self.ui.tableWidget.setHorizontalHeaderLabels(df.columns)

            for i in range (len(df.index)):
                for j in range (len(df.columns)):
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(df.iat[i,j])))

            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(0)
        except:
            pass

    # Отображение всех данных
    def showalldb(self):
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT sensors.name, sensors.serial_number, type_sensors.type,
            observations.date, observations.time, temperature.temperature,
            observations.mark
            FROM observations
            JOIN sensors ON sensors.uid_sensor = observations.uid_sensor
            JOIN type_sensors ON sensors.uid_type = type_sensors.uid_type
            JOIN temperature ON temperature.uid_observations = observations.uid_observations
            """
        )


        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Название', 'Серийный номер', 'Тип датчика', 'Дата', 'Время', 'Температура'])
        while Query.next():
            rows = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.setRowCount(rows + 1)
            i = 0
            for i in range(6):
                self.ui.tableWidget.setItem(rows, i, QTableWidgetItem(str(Query.value(i))))
            if Query.value(6) == 1:
                self.ui.tableWidget.setItem(rows, 6, QTableWidgetItem(str("Верно")))
            else:
                self.ui.tableWidget.setItem(rows, 6, QTableWidgetItem(str("Ошибка данных")))
        
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(0)

    # Открытие окна с сотношением столбцов
    def showadata(self):
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT uid_sensor, name, serial_number, N_S, E_W, location FROM sensors
            """
        )

        sens = {}

        while Query.next():
            sens[Query.value(0)] =str(Query.value(1)) + ' | ' + str(Query.value(2)) + ' | ' + str(Query.value(5))

        headers = {}
        headers[100] = ' '
        try:
            heads = list(self.df.columns)
            k = 0
            for i in heads:
                headers[k] = i
                k +=1
        except:
            pass



        addwindow = adddatatodb.Adddatatodb(self, sens, headers)
        addwindow.exec_()

        sensor = addwindow.sensor
        date = addwindow.date
        time = addwindow.time
        tempair = addwindow.tempair

        try:
            for i in range (len(self.df.index)):
                Query.exec(
                    f"""
                    INSERT INTO observations (uid_sensor, date, time)
                    VALUES ({sensor}, '{str(self.df.iat[i,date])}', '{str(self.df.iat[i,time])}') 
                    """
                )

                Query.exec(
                    """
                    SELECT uid_observations FROM observations WHERE uid_observations = (SELECT MAX(uid_observations)  FROM observations)
                    """
                )

                while Query.next():
                    id = Query.value(0)
                
                Query.exec(
                    f"""
                    INSERT INTO temperature (uid_observations, temperature)
                    VALUES ({int(id)}, {float(self.df.iat[i,tempair])}) 
                    """
                )

                # print(str(self.df.iat[i,time]))
        except:
            pass


        

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