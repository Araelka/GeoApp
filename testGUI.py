from GUImainwindowd import Ui_MainWindow
import map
import sys
from statistics import mean
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QHeaderView,
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QStyle,
    QTableWidgetItem,
)
import pandas as pd

import addsensor
import adddatatodb
import checkdata

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.showtable)
        self.ui.show_map_sensors_action.triggered.connect(self.showmap)
        self.ui.add_sensor_action.triggered.connect(self.add_sens)
        self.ui.show_senssors_action.triggered.connect(self.showsensor)
        self.ui.load_action.triggered.connect(self.uploadfile)
        self.ui.add_data_to_DB_action.triggered.connect(self.loadfiletoDB)
        self.ui.dateTimeEdit_max.setDateTime(QtCore.QDateTime().currentDateTime())
        sensors = self.sensors()
        for i in sensors:
            self.ui.sensors_comboBox.addItem(sensors[i], i)
        typetable = self.typetable()
        for i in typetable:
            self.ui.type_comboBox.addItem(i, typetable[i])
        self.ui.tableWidget.viewport().installEventFilter(self) # для фильтрации кнопок
        self.ui.max_action.triggered.connect(self.MAX)
        self.ui.min_action.triggered.connect(self.MIN)
        self.ui.mean_action.triggered.connect(self.MEAN)


    # Фильтр на нажание кнопой ЛЕвая или правая
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                return 0
            elif event.button() == QtCore.Qt.RightButton:
                print("Правая")
        return super().eventFilter(source, event)


    
    # Загрузка данных из в файла в dataframe
    def uploadfile(self):
        filename = QFileDialog.getOpenFileName(self, 'Открыть файл', '*.csv')
        
        if filename[0]:
            try:
                self.df = pd.read_csv(filename[0], skiprows = 1)
                self.df = self.df.loc[0:20]
            except:
                return 0
            self.df = self.df.drop(columns = self.df.columns[0])
            self.df[self.df.columns[0]] = pd.to_datetime(self.df[self.df.columns[0]])
            # Изменить формат даты и времени
            self.df.insert(0, 'Time, GMT+07:00', self.df['Date Time, GMT+07:00'].dt.time)
            self.df.insert(0, 'Date, GMT+07:00', self.df['Date Time, GMT+07:00'].dt.date)
            self.df = self.df.drop(columns=self.df.columns[2])
            self.showlastfile(self.df)


    # Получение всех датчиков
    def sensors(self):
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT sensors.uid_sensor, sensors.name, sensors.serial_number, type_sensors.type, sensors.location
            FROM sensors
            JOIN type_sensors ON sensors.uid_type = type_sensors.uid_type;
            """
        )

        sensors = {}
        sensors[-1] = 'Все'
        while Query.next():
            sensors[Query.value(0)] = str(Query.value(1)) + ' | ' + str(Query.value(2)) + ' | ' + str(Query.value(3)) + ' | ' + str(Query.value(4))

        return sensors
    
    # Типы таблицы
    def typetable(self):
        typename = ['Water Content, m³/m³', 'Current, mA', 'PAR, µmol/m²/s', 'Temperature Air, °C', 'RH, %', 
                    'Wind Speed, mph', 'Gust Speed, mph', 'Wind Direction,  ø', 'Temperature Ground, °C',
                    'Pressure, Hg', 'Rain', 'Solar Radiation, W/m²']
        
        tablename = ['water_content', 'current', 'PAR', 'temperature_air', 'RH', 
                     'wind_speed', 'gust_speed', 'wind_direction', 'temperature_ground',
                     'pressure', 'rain', 'solar_radiation']
        
        typetb = {}
        typetb['Все'] = 'Все'
        j = 0
        for i in typename:
            typetb[i] = tablename[j]
            j += 1

        return typetb

# 
    # Отрисовка последнего или переданного datafrema
    def showlastfile(self, df):
        self.ui.tableWidget.clear()
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

            # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            # self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(0)
        except:
            pass



    # Отображение всех данных с возможностью выборки
    def showtable(self):
        Query = QSqlQuery()

        if self.ui.date_checkBox.isChecked() == True:
            datacheck = f"WHERE datetime(observations.date,  observations.time) >= '{self.ui.dateTimeEdit_min.dateTime().toPyDateTime()}' AND datetime(observations.date, observations.time) <= '{self.ui.dateTimeEdit_max.dateTime().toPyDateTime()}'"
            ch = 1
        else:
            datacheck = ''
            ch = 0

        if self.ui.sensor_checkBox.isChecked() == True and int(self.ui.sensors_comboBox.currentData()) > -1:
            if ch == 1:
                w = 'AND'
            else:
                w = 'WHERE'
            sensorcheck = f"{w} sensors.uid_sensor == {int(self.ui.sensors_comboBox.currentData())}"
            ch = 1
        else:
            sensorcheck = ''
            ch = 0

        if self.ui.type_checkBox.isChecked() == True and str(self.ui.type_comboBox.currentData()) != 'Все':   
            if ch == 1:
                w = "AND"
            else:
                w = "WHERE"
            datetype = f"{str(self.ui.type_comboBox.currentData())}.value,"
            typecheck = f"JOIN {str(self.ui.type_comboBox.currentData())} ON {str(self.ui.type_comboBox.currentData())}.uid_observations = observations.uid_observations"
            NH = 9
        else:
            datetype = """
            water_content.value, current.value, PAR.value, temperature_air.value,
            RH.value, wind_speed.value, gust_speed.value, wind_direction.value,
            temperature_ground.value, pressure.value, rain.value, solar_radiation.value,
            """

            typecheck = """
            LEFT JOIN water_content ON water_content.uid_observations = observations.uid_observations
            LEFT JOIN current ON current.uid_observations = observations.uid_observations
            LEFT JOIN PAR ON PAR.uid_observations = observations.uid_observations
            LEFT JOIN temperature_air ON temperature_air.uid_observations = observations.uid_observations
            LEFT JOIN RH ON RH.uid_observations = observations.uid_observations
            LEFT JOIN wind_speed ON wind_speed.uid_observations = observations.uid_observations
            LEFT JOIN gust_speed ON gust_speed.uid_observations = observations.uid_observations
            LEFT JOIN wind_direction ON wind_direction.uid_observations = observations.uid_observations
            LEFT JOIN temperature_ground ON temperature_ground.uid_observations = observations.uid_observations
            LEFT JOIN pressure ON pressure.uid_observations = observations.uid_observations
            LEFT JOIN rain ON rain.uid_observations = observations.uid_observations
            LEFT JOIN solar_radiation ON solar_radiation.uid_observations = observations.uid_observations"""
        
            NH = 20


        Query.exec(
            f"""
            SELECT observations.mark, observations.uid_observations,
            sensors.name, sensors.serial_number, type_sensors.type,
            observations.date, observations.time, 
            {datetype}
            observations.mark
            FROM observations
            LEFT JOIN sensors ON sensors.uid_sensor = observations.uid_sensor
            LEFT JOIN type_sensors ON sensors.uid_type = type_sensors.uid_type
            {typecheck}
            {datacheck}
            {sensorcheck}
            """
        )

        # print(Query.executedQuery())


        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(NH)
        if NH == 20:
            self.ui.tableWidget.setHorizontalHeaderLabels([' ', '№', 'Датчик', 'Серийный номер', 'Тип датчика', 'Дата', 'Время', 
                                                        'Water Content, m³/m³', 'Current, mA', 'PAR, µmol/m²/s', 'Temperature Air, °C', 'RH, %', 
                                                        'Wind Speed, mph', 'Gust Speed, mph', 'Wind Direction,  ø', 'Temperature Ground, °C',
                                                        'Pressure, Hg', 'Rain', 'Solar Radiation, W/m²', 'Корректность'])
        else:
            self.ui.tableWidget.setHorizontalHeaderLabels([' ', '№', 'Датчик', 'Серийный номер', 'Тип датчика', 'Дата', 'Время', 
                                                        f'{str(self.ui.type_comboBox.currentText())}', 'Корректность'])

        

        # Изменение метки корректности
        def changeS():
            row = self.ui.tableWidget.currentRow()
            id = int(self.ui.tableWidget.item(row, 1).text())
            if CheckBox[row].isChecked() == True:
                mark = 1
                self.ui.tableWidget.setItem(row, (NH-1), QTableWidgetItem(str("Верно")))
                if row%2 ==1:
                    self.ui.tableWidget.item(row, (NH-1)).setBackground(QtGui.QColor(202, 204, 206))
            else:
                mark = 0
                self.ui.tableWidget.setItem(row, (NH-1), QTableWidgetItem(str("Ошибка")))
                if row%2 ==1:
                    self.ui.tableWidget.item(row, (NH-1)).setBackground(QtGui.QColor(202, 204, 206))

            Query.exec(
                f"""
                UPDATE observations
                SET mark = {mark}
                WHERE uid_observations = {id}
                """
            )

        CheckBox = []

        try:
            while Query.next():
                CheckBox.append(QtWidgets.QCheckBox())
                rows = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.setRowCount(rows + 1)
                i = 0
                for i in range(NH):
                    self.ui.tableWidget.setItem(rows, i, QTableWidgetItem(str(Query.value(i))))
                    if rows%2 ==1:
                        self.ui.tableWidget.item(rows, i).setBackground(QtGui.QColor(202, 204, 206))
    
                if Query.value(0) == 1:
                    self.ui.tableWidget.setItem(rows, (NH-1), QTableWidgetItem(str("Верно")))
                    if rows%2 ==1:
                        self.ui.tableWidget.item(rows, (NH-1)).setBackground(QtGui.QColor(202, 204, 206))
                    CheckBox[-1].setChecked(True)
                    self.ui.tableWidget.setCellWidget(rows, 0, CheckBox[-1])
                    CheckBox[-1].stateChanged.connect(changeS)
                else:
                    self.ui.tableWidget.setItem(rows, (NH-1), QTableWidgetItem(str("Ошибка")))
                    if rows%2 ==1:
                        self.ui.tableWidget.item(rows, (NH-1)).setBackground(QtGui.QColor(202, 204, 206))
                    self.ui.tableWidget.setCellWidget(rows, 0, CheckBox[-1])
                    CheckBox[-1].stateChanged.connect(changeS)
                
                # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                # self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(0)

        except:
            QMessageBox.about(self, "Данные", "Произошла ошибка отображения")
    
        
    def MAX(self):
        max_list = []
        column = self.ui.tableWidget.currentColumn()
        rows = self.ui.tableWidget.rowCount()
        try:
            for row in range(rows):
                if self.ui.tableWidget.item(row, column).text() != '':
                    max_list.append(float(self.ui.tableWidget.item(row, column).text()))
            mbox = QMessageBox()
            mbox.setText("Максимум по "+ str(self.ui.tableWidget.horizontalHeaderItem(column).text())+ ": " + str(max(max_list)))
            mbox.setWindowTitle("Максимум")
            mbox.exec_()
        except:
            pass

    def MIN(self):
        min_list = []
        column = self.ui.tableWidget.currentColumn()
        rows = self.ui.tableWidget.rowCount()
        try:
            for row in range(rows):
                if self.ui.tableWidget.item(row, column).text() != '':
                    min_list.append(float(self.ui.tableWidget.item(row, column).text()))
            mbox = QMessageBox()
            mbox.setText("Минимум по "+ str(self.ui.tableWidget.horizontalHeaderItem(column).text())+ ": " + str(min(min_list)))
            mbox.setWindowTitle("Минимум")
            mbox.exec_()
        except:
            pass

    def MEAN(self):
        mean_list = []
        column = self.ui.tableWidget.currentColumn()
        rows = self.ui.tableWidget.rowCount()
        try:
            for row in range(rows):
                if self.ui.tableWidget.item(row, column).text() != '':
                    mean_list.append(float(self.ui.tableWidget.item(row, column).text()))
            mbox = QMessageBox()
            mbox.setText("Среднее по "+ str(self.ui.tableWidget.horizontalHeaderItem(column).text())+ ": " + str(round(mean(mean_list), 2)))
            mbox.setWindowTitle("Среднее")
            mbox.exec_()
        except:
            pass

    # Открытие окна с сотношением столбцов и загрузка в базу
    def loadfiletoDB(self):
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

        windowdate = adddatatodb.Adddatatodb(self, sens, headers)
        windowdate.exec_()

        checkwindow = checkdata.DataCheck(self)
        checkwindow.exec_()

        try:
            temp_check = checkwindow.temp
            RH_check = checkwindow.RH
        except:
            pass
        
        try:
            sensor = windowdate.sensor
            date = windowdate.date
            time = windowdate.time
        except:
            pass
        try:
            water_content = windowdate.water_content
        except:
            pass
        try:
            current = windowdate.current
        except:
            pass
        try:
            PAR = windowdate.PAR
        except:
            pass
        try:
            temp_air = windowdate.temp_air
            airtype = windowdate.airtype
        except:
            pass
        try:
            RH = windowdate.RH
        except:
            pass
        try:
            wind_speed = windowdate.wind_speed
        except:
            pass
        try:
            gust_speed = windowdate.gust_speed
        except:
            pass
        try:
            wind_direction = windowdate.wind_direction
        except:
            pass
        try:
            temp_ground = windowdate.temp_ground
            groundtype = windowdate.groundtype
        except:
            pass
        try:
            pressure = windowdate.pressure
        except:
            pass
        try:
            rain = windowdate.rain
        except:
            pass
        try:
            solar_radiation = windowdate.solar_radiation
        except:
            pass

        try:
            for i in range (len(self.df.index)):
                # Загрузка наблюдений
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
                
                # Загрузка temperature_air
                try:
                    if airtype == 1:
                        temp = float(self.df.iat[i,temp_air])
                        if temp < temp_check[0] or temp > temp_check[1]:
                            Query.exec(
                            f"""
                            UPDATE observations
                            SET mark = 0
                            WHERE uid_observations = {id}
                            """
                        )



                        Query.exec(
                            f"""
                            INSERT INTO temperature_air (uid_observations, value)
                            VALUES ({int(id)}, {round(temp, 1)}) 
                            """
                        )
                    else:
                        temp = float((5/9)*(float(self.df.iat[i,temp_air])-32))
                        if temp < temp_check[0] or temp > temp_check[1]:
                            Query.exec(
                            f"""
                            UPDATE observations
                            SET mark = 0
                            WHERE uid_observations = {id}
                            """
                        )


                        Query.exec(
                            f"""
                            INSERT INTO temperature_air (uid_observations, value)
                            VALUES ({int(id)}, {round(temp, 1)}) 
                            """
                        )
                except:
                    pass
                
                # Загрузка RH
                try:
                    if float(self.df.iat[i,RH]) < RH_check[0] or float(self.df.iat[i,RH]) > RH_check[1]:
                        Query.exec(
                        f"""
                        UPDATE observations
                        SET mark = 0
                        WHERE uid_observations = {id}
                        """
                    )


                    Query.exec(
                        f"""
                        INSERT INTO RH (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,RH])}) 
                        """
                    )
                except:
                    pass

                # Загрузка water_content
                try:
                    Query.exec(
                        f"""
                        INSERT INTO water_content (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,water_content])}) 
                        """
                    )
                except:
                    pass

                # Загрузка PAR
                try:
                    Query.exec(
                        f"""
                        INSERT INTO PAR (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,PAR])}) 
                        """
                    )
                except:
                    pass

                # Загрузка rain
                try:
                    Query.exec(
                        f"""
                        INSERT INTO rain (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,rain])}) 
                        """
                    )
                except:
                    pass

                # Загрузка current
                try:
                    Query.exec(
                        f"""
                        INSERT INTO current (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,current])}) 
                        """
                    )
                except:
                    pass

                # Загрузка pressure
                try:
                    Query.exec(
                        f"""
                        INSERT INTO pressure (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,pressure])}) 
                        """
                    )
                except:
                    pass

                # Загрузка gust_speed
                try:
                    Query.exec(
                        f"""
                        INSERT INTO gust_speed (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,gust_speed])}) 
                        """
                    )
                except:
                    pass

                # Загрузка wind_speed
                try:
                    Query.exec(
                        f"""
                        INSERT INTO wind_speed (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,wind_speed])}) 
                        """
                    )
                except:
                    pass

                # Загрузка solar_radiation
                try:
                    Query.exec(
                        f"""
                        INSERT INTO solar_radiation (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,solar_radiation])}) 
                        """
                    )
                except:
                    pass

                # Загрузка wind_direction
                try:
                    Query.exec(
                        f"""
                        INSERT INTO wind_direction (uid_observations, value)
                        VALUES ({int(id)}, {float(self.df.iat[i,wind_direction])}) 
                        """
                    )
                except:
                    pass

                # Загрузка temperature_ground
                try:
                    if groundtype == 1:
                        temp = float(self.df.iat[i,temp_ground])
                        if temp < temp_check[0] or temp > temp_check[1]:
                            Query.exec(
                            f"""
                            UPDATE observations
                            SET mark = 0
                            WHERE uid_observations = {id}
                            """
                            )


                        Query.exec(
                            f"""
                            INSERT INTO temperature_ground (uid_observations, value)
                            VALUES ({int(id)}, {round(temp, 3)}) 
                            """
                        )
                    else:
                        temp = float((5/9)*(float(self.df.iat[i,temp_ground])-32))
                        if temp < temp_check[0] or temp > temp_check[1]:
                            Query.exec(
                            f"""
                            UPDATE observations
                            SET mark = 0
                            WHERE uid_observations = {id}
                            """
                            )

                        Query.exec(
                            f"""
                            INSERT INTO temperature_ground (uid_observations, value)
                            VALUES ({int(id)}, {round(temp, 3)}) 
                            """
                        )
                except:
                    pass
            QMessageBox.about(self, "Загрузка данных", "Данные успешно загружены")
        except:
            QMessageBox.about(self, "Загрузка данных", "Не удалось загрузить данные\nПроверьте сотношение столбцов")


        
    # Показать датчики из базы
    def showsensor(self):
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
                if rows%2 ==1:
                    self.ui.tableWidget.item(rows, i).setBackground(QtGui.QColor(202, 204, 206))
        
        # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(0)

    # Нахождение координат датчиков
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

    # Карта с датчиками
    def showmap(self):
        new_map = map.Map(coords = self.coords_sens())
        new_map.exec_()

    # Открытие окна с добавлением датчика
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


    # Добавление датчика в базу данных
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



# Соединение с базой данных
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