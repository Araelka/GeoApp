from GUImainwindow import Ui_MainWindow
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
import matplotlib.pyplot as plt   
from datetime import datetime, date
from xlsxwriter.workbook import Workbook 

import addsensor
import adddatatodb
import checkdata
import map

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
        true = ['Все','Корректные', 'Некорректные']
        for i in range(-1,2):
            self.ui.true_comboBox.addItem(true[i+1], i)
        # self.ui.tableWidget.viewport().installEventFilter(self) # для фильтрации кнопок
        self.ui.max_action.triggered.connect(self.MAX)
        self.ui.min_action.triggered.connect(self.MIN)
        self.ui.mean_action.triggered.connect(self.MEAN)
        # self.ui.plot_action.triggered.connect(self.ShowPlot)
        self.ui.plot_action.triggered.connect(self.testFunc)
        self.ui.day_action.triggered.connect(self.DayGroup)
        self.ui.week_action.triggered.connect(self.WeekGroup)
        self.ui.month_action.triggered.connect(self.MonthGroup)
        self.ui.save_action.triggered.connect(self.SaveFile)
        


    # Требуется доработка
    # Устойчивый переход температуры через заданный рубеж
    def testFunc(self):
        rows = self.ui.tableWidget.rowCount()
        headers = []
        for column in range(self.ui.tableWidget.columnCount()):
            headers.append(self.ui.tableWidget.horizontalHeaderItem(column).text())
        try:
            temperature = headers.index("Temperature Air, °C")
            date = headers.index("Дата")
            time = headers.index('Время')
        except:
            return
        max = 0
        min = 0

        df = {"Дата": [], "Temperature Air, °C": []}
        df = pd.DataFrame(df)

        for row in range(rows):
            if self.ui.tableWidget.item(row , temperature).text() != '' and self.ui.tableWidget.item(row , 0).text() == '1':
                row_a = [datetime.strptime(self.ui.tableWidget.item(row , date).text() + ' ' + self.ui.tableWidget.item(row , time).text(), '%Y-%m-%d %H:%M:%S'), 
                         float(self.ui.tableWidget.item(row , temperature).text())]
                df.loc[len(df.index)] = row_a

        res = df.groupby(pd.Grouper(key=df.columns[0], freq='D')).mean().reset_index()
        res['Дата'] = pd.to_datetime(res["Дата"]).dt.date
        res = res.round(5)

        date = ''
        count = 0
        excount = 0
        e = 7
        temperature = 0
        for i in res.index:
            if res['Temperature Air, °C'][i] < temperature and date == '' and excount <= e:
                # print(res['Temperature Air, °C'][i])
                count += 1
                date = str(res['Дата'][i])
            elif res['Temperature Air, °C'][i] < temperature and date != '' and excount <= e:
                count += 1
            elif res['Temperature Air, °C'][i] > temperature:
                excount += 1
                # count -= 1
            if excount > e:
                excount = 0
                count = 0
                date = ''
            if count >= 15:
                print(date, count, excount)
                break
        # print(res.index)
        # print(res)
        

    # Фильтр на нажание кнопой ЛЕвая или правая
    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.MouseButtonPress:
    #         if event.button() == QtCore.Qt.LeftButton:
    #             return 0
    #         elif event.button() == QtCore.Qt.RightButton:
    #             pass
    #     return super().eventFilter(source, event)


    
    # Загрузка данных из в файла в dataframe
    def uploadfile(self):
        filename = QFileDialog.getOpenFileName(self, 'Открыть файл', '*.csv')
        
        if filename[0]:
            try:
                self.df = pd.read_csv(filename[0], skiprows = 1)
                # self.df = self.df.loc[0:1000]
            except:
                return 0
            self.df = self.df.drop(columns = self.df.columns[0])
            self.df[self.df.columns[0]] = pd.to_datetime(self.df[self.df.columns[0]])
            # Изменить формат даты и времени
            self.df.insert(0, 'Time, GMT+07:00', self.df['Date Time, GMT+07:00'].dt.time)
            self.df.insert(0, 'Date, GMT+07:00', self.df['Date Time, GMT+07:00'].dt.date)
            self.df = self.df.drop(columns=self.df.columns[2])
            self.showlastfile(self.df)


    # Сохранение данных из таблицы в файл
    def SaveFile(self):
        fileName, ok = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            ".",
            "All Files(*.xlsx)"
        )
        if not fileName:
            return 
        
        try:
            list_tabel = []
            rows = self.ui.tableWidget.rowCount()
            columns = self.ui.tableWidget.columnCount()
            headers = []
            for column in range(2, columns):
                headers.append("{}".format(self.ui.tableWidget.horizontalHeaderItem(column).text() or ""))
            list_tabel.append(headers)


            for row in range(rows):
                row_tabel = []
                for column in range(2, columns):
                    row_tabel.append("{}".format(self.ui.tableWidget.item(row, column).text() or ""))
                list_tabel.append(row_tabel)

            workbook = Workbook(fileName)
            worksheet = workbook.add_worksheet() 

            for r, row in enumerate(list_tabel):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)        
            workbook.close()  
            msg = QMessageBox.information(
                self, 
                "Успех!", 
                f"Данные сохранены в файле: \n{fileName}"
            ) 
        except:
            return

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
        typename = ['Water Content, m³/m³', 'PAR, µmol/m²/s', 'Temperature Air, °C', 'RH, %', 
                    'Wind Speed, mph', 'Gust Speed, mph', 'Wind Direction,  ø', 'Temperature Ground, °C',
                    'Pressure, Hg', 'Rain', 'Solar Radiation, W/m²']
        
        tablename = ['water_content', 'PAR', 'temperature_air', 'RH', 
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



    # Отрисовка графиков
    def ShowPlot(self):
        tempdate = []
        column = self.ui.tableWidget.currentColumn()
        rows = self.ui.tableWidget.rowCount()
        tempframe = []
        try:
            for row in range (rows):
                if self.ui.tableWidget.item(row, column).text() != '':
                    tempdate.append(datetime.strptime(self.ui.tableWidget.item(row , 5).text() + ' ' + self.ui.tableWidget.item(row , 6).text(), '%Y-%m-%d %H:%M:%S'))
                    tempframe.append(float(self.ui.tableWidget.item(row , column).text()))
            plt.plot(tempdate, tempframe, label = self.ui.tableWidget.horizontalHeaderItem(column).text())
            # for row in range(rows):
            #     if self.ui.tableWidget.item(row, column).text() != '':
                    # for j in range (self.ui.tableWidget.rowCount()):
                    # tempframe.append(float(self.ui.tableWidget.item(row , column).text()))
                    # plt.plot(tempframe)
  
            plt.title("График " + self.ui.tableWidget.horizontalHeaderItem(column).text())
            plt.xticks(rotation = 90)
            plt.xlabel(self.ui.tableWidget.horizontalHeaderItem(5).text() + ' ' + self.ui.tableWidget.horizontalHeaderItem(6).text())
            plt.ylabel(self.ui.tableWidget.horizontalHeaderItem(column).text()) # Ошибка, не может получить текст
            plt.legend()
            #plt.get_current_fig_manager().window.showMaximized() - развернуть график на весь экран по умолчанию
            plt.show()
        except:
            pass

    # Отображение всех данных с возможностью выборки
    def showtable(self):
        Query = QSqlQuery()

        # Выбор по дате
        if self.ui.date_checkBox.isChecked() == True:
            datacheck = f"WHERE datetime(observations.date,  observations.time) >= '{self.ui.dateTimeEdit_min.dateTime().toPyDateTime()}' AND datetime(observations.date, observations.time) <= '{self.ui.dateTimeEdit_max.dateTime().toPyDateTime()}'"
            ch = 1
        else:
            datacheck = ''
            ch = 0

        # Выбор по датчику
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

        # Выбор по корректности
        if self.ui.true_checkBox.isChecked() == True and int(self.ui.true_comboBox.currentData()) > -1:
            if ch == 1:
                w = 'AND'
            else:
                w = 'WHERE'
            if int(self.ui.true_comboBox.currentData()) == 0:
                truecheck = f"{w} observations.mark == {int(self.ui.true_comboBox.currentData()+1)}"
            else:
                truecheck = f"{w} observations.mark == {int(self.ui.true_comboBox.currentData()-1)}"
            ch = 1
        else:
            truecheck = ''
            ch = 0    

        # Выбор по типу данных
        if self.ui.type_checkBox.isChecked() == True and str(self.ui.type_comboBox.currentData()) != 'Все':   
            if ch == 1:
                w = "AND"
            else:
                w = "WHERE"
            datetype = f"observations.{str(self.ui.type_comboBox.currentData())},"
            # typecheck = f"JOIN {str(self.ui.type_comboBox.currentData())} ON {str(self.ui.type_comboBox.currentData())}.uid_observations = observations.uid_observations"
            NH = 9
        else:
            datetype = """
            observations.water_content, observations.PAR, observations.temperature_air,
            observations.RH, observations.wind_speed, observations.gust_speed, observations.wind_direction,
            observations.temperature_ground, observations.pressure, observations.rain, observations.solar_radiation,
            """

            # typecheck = """
            # LEFT JOIN water_content ON water_content.uid_observations = observations.uid_observations
            # LEFT JOIN current ON current.uid_observations = observations.uid_observations
            # LEFT JOIN PAR ON PAR.uid_observations = observations.uid_observations
            # LEFT JOIN temperature_air ON temperature_air.uid_observations = observations.uid_observations
            # LEFT JOIN RH ON RH.uid_observations = observations.uid_observations
            # LEFT JOIN wind_speed ON wind_speed.uid_observations = observations.uid_observations
            # LEFT JOIN gust_speed ON gust_speed.uid_observations = observations.uid_observations
            # LEFT JOIN wind_direction ON wind_direction.uid_observations = observations.uid_observations
            # LEFT JOIN temperature_ground ON temperature_ground.uid_observations = observations.uid_observations
            # LEFT JOIN pressure ON pressure.uid_observations = observations.uid_observations
            # LEFT JOIN rain ON rain.uid_observations = observations.uid_observations
            # LEFT JOIN solar_radiation ON solar_radiation.uid_observations = observations.uid_observations"""
        
            NH = 19


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
            {datacheck}
            {sensorcheck}
            {truecheck}
            """
        )

        # print(Query.executedQuery())


        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(NH)
        if NH == 19:
            self.ui.tableWidget.setHorizontalHeaderLabels([' ', '№', 'Датчик', 'Серийный номер', 'Тип датчика', 'Дата', 'Время', 
                                                        'Water Content, m³/m³', 'PAR, µmol/m²/s', 'Temperature Air, °C', 'RH, %', 
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
                rows = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.setRowCount(rows + 1)
                i = 0
                for i in range(NH):
                    self.ui.tableWidget.setItem(rows, i, QTableWidgetItem(str(Query.value(i))))
                    if rows%2 ==1:
                        self.ui.tableWidget.item(rows, i).setBackground(QtGui.QColor(202, 204, 206))

            for rows in range(self.ui.tableWidget.rowCount()):
                CheckBox.append(QtWidgets.QCheckBox())
                if int(self.ui.tableWidget.item(rows, 0).text()) == 1:
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
                
                
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(0)

        except:
            QMessageBox.about(self, "Данные", "Произошла ошибка отображения")
            return
    
        
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
        headers[-1] = ' '
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
        
        if windowdate.isClose == 0:
            return 0

        checkwindow = checkdata.DataCheck(self)
        checkwindow.exec_()

        temp_check = checkwindow.temp
        RH_check = checkwindow.RH
        
        data_dict_W = windowdate.data_dict
        type_dict_W = windowdate.type_dict
        data_dict = {}
        value_dict = {}
        for i in data_dict_W:
            if data_dict_W[i] != -1 and i in ['uid_sensor', 'date', 'time']:
                data_dict[i] = data_dict_W[i]
            elif data_dict_W[i] != -1 and i not in ['uid_sensor', 'date', 'time']:
                value_dict[i] = data_dict_W[i]

        tabel_name_data = ', '.join(data_dict)
        tabel_name_value = ', '.join(value_dict)


                

        try:
            for i in range (len(self.df.index)):
                value = []
                for name in value_dict:
                    # print(type_dict_W['air_type'])
                    if name not in ['temperature_air', 'temperature_ground', 'RH']:
                        value.append(float(self.df.iat[i,value_dict[f'{name}']]))

                    elif name in ['temperature_air'] and type_dict_W['air_type'] == 0:
                        temperature = float((5/9)*(float(self.df.iat[i,value_dict[f'{name}']])-32))
                        value.append(round(float(temperature), 3))
                    elif name in ['temperature_air'] and type_dict_W['air_type'] == 1:
                        temperature = float(self.df.iat[i,value_dict[f'{name}']])
                        value.append(round(float(temperature), 3))

                    elif name in ['temperature_ground'] and type_dict_W['ground_type'] == 0:
                        temperature = float((5/9)*(float(self.df.iat[i,value_dict[f'{name}']])-32))
                        value.append(round(float(temperature), 3))
                    elif name in ['temperature_ground'] and type_dict_W['ground_type'] == 1:
                        temperature = float(self.df.iat[i,value_dict[f'{name}']])
                        value.append(round(float(temperature), 3))
                    
                    elif name in ['RH']:
                        RH = float(self.df.iat[i,value_dict[f'{name}']])
                        value.append(float(RH))
                
                # print(value)
                
                    
                count = len(value)

                # Загрузка наблюдений
                match count:
                    case 11:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]}, {value[6]}, {value[7]}, {value[8]}, {value[9]}, {value[10]})
                            """
                        )
                    case 10:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]}, {value[6]}, {value[7]}, {value[8]}, {value[9]})
                            """
                        )
                    case 9:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]}, {value[6]}, {value[7]}, {value[8]})
                            """
                        )
                    case 8:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]}, {value[6]}, {value[7]})
                            """
                        )
                    case 7:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]}, {value[6]})
                            """
                        )
                    case 6:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]}, {value[5]})
                            """
                        )
                    case 5:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]}, {value[4]})
                            """
                        )
                    case 4:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]}, {value[3]})
                            """
                        )
                    case 3:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]}, {value[2]})
                            """
                        )
                    case 2:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]}, {value[1]})
                            """
                        )
                    case 1:
                        Query.exec(
                            f"""
                            INSERT INTO observations ({tabel_name_data}, {tabel_name_value})
                            VALUES ({data_dict['uid_sensor']}, '{str(self.df.iat[i,data_dict['date']])}', '{str(self.df.iat[i,data_dict['time']])}',
                            {value[0]})
                            """
                        )
                    
                self.DBcheck(temp_check, RH_check)

            QMessageBox.about(self, "Загрузка данных", "Данные успешно загружены")

        except:
            QMessageBox.about(self, "Загрузка данных", "Не удалось загрузить данные\nПроверьте сотношение столбцов")
            

    #  Проверка ограничений входных данных из файла  
    def DBcheck(self, temp_check, RH_check):
        Query = QSqlQuery()
        Query.exec(
            """
            SELECT uid_observations, temperature_air, temperature_ground, RH 
            FROM observations 
            WHERE uid_observations = (SELECT MAX(uid_observations)  FROM observations)
            """
        )

        while Query.next():
            if Query.value(1) < temp_check[0] or Query.value(1) > temp_check[1]:
                id = Query.value(0)
            elif Query.value(2) < temp_check[0] or Query.value(2) > temp_check[1]:
                id = Query.value(0)
            elif Query.value(3) < RH_check[0] or Query.value(3) > RH_check[1]:
                id = Query.value(0)
            else:
                return

            Query.exec(
                f"""
                UPDATE observations
                SET mark = 0
                WHERE uid_observations = {id}
                """
            )


    def DayGroup(self):
        self.DateGroup('D')
    
    def WeekGroup(self):
        self.DateGroup('W')

    def MonthGroup(self):
        self.DateGroup('M')


    # Срочные данные (День, неденя, месяц)
    def DateGroup(self, typegroup):
        try:
            df = {"Дата": [], "Temperature Air, °C": []}
            df_g = {"Дата": [], "Temperature Ground, °C": []}
            df = pd.DataFrame(df)
            df_g = pd.DataFrame(df_g)
            rows = self.ui.tableWidget.rowCount()
            columns = self.ui.tableWidget.columnCount()
            headers = []
            for column in range(columns):
                headers.append(self.ui.tableWidget.horizontalHeaderItem(column).text())
            sensor = headers.index('Датчик')
            date = headers.index('Дата')
            time = headers.index('Время')
            try:
                col_air = headers.index("Temperature Air, °C")
            except:
                pass
            try:
                col_ground = headers.index("Temperature Ground, °C")
            except:
                pass

            try:
                for row in range(rows):
                    if self.ui.tableWidget.item(row , col_air).text() != '' and self.ui.tableWidget.item(row , 0).text() == '1':
                        row_a = [datetime.strptime(self.ui.tableWidget.item(row , date).text() + ' ' + self.ui.tableWidget.item(row , time).text(), '%Y-%m-%d %H:%M:%S'), 
                        float(self.ui.tableWidget.item(row , col_air).text())]
                        df.loc[len(df.index)] = row_a
                    else:
                        pass
            except:
                pass
            
            try:
                for row in range(rows):
                    if self.ui.tableWidget.item(row , col_ground).text() != '' and self.ui.tableWidget.item(row , 0).text() == '1':
                        row_g = [datetime.strptime(self.ui.tableWidget.item(row , date).text() + ' ' + self.ui.tableWidget.item(row , time).text(), '%Y-%m-%d %H:%M:%S'), 
                        float(self.ui.tableWidget.item(row , col_ground).text())]
                        df_g.loc[len(df_g.index)] = row_g
                    else:
                        pass
            except:
                pass
            
            try:
                res_min = df.groupby(pd.Grouper(key=df.columns[0], freq=f'{typegroup}'))[df.columns[1]].min().reset_index()
                res = df.groupby(pd.Grouper(key=df.columns[0], freq=f'{typegroup}')).mean().reset_index()
                res_max = df.groupby(pd.Grouper(key=df.columns[0], freq=f'{typegroup}'))[df.columns[1]].max().reset_index()

                res['Дата'] = pd.to_datetime(res["Дата"]).dt.date
                res = res.round(2)
                res_min = res_min.round(2)
                res_max = res_max.round(2)
            except:
                res = pd.DataFrame()
                N = 4
                pass

            try:
                res_min_g = df_g.groupby(pd.Grouper(key=df_g.columns[0], freq=f'{typegroup}'))[df_g.columns[1]].min().reset_index()
                res_g = df_g.groupby(pd.Grouper(key=df_g.columns[0], freq=f'{typegroup}'))[df_g.columns[1]].mean().reset_index()
                res_max_g = df_g.groupby(pd.Grouper(key=df_g.columns[0], freq=f'{typegroup}'))[df_g.columns[1]].max().reset_index()

                res_g['Дата'] = pd.to_datetime(res_g["Дата"]).dt.date
                res_g = res_g.round(2)
                res_min_g = res_min_g.round(2)
                res_max_g = res_max_g.round(2)
            except:
                res_g = pd.DataFrame()
                N = 4
                pass
            
            # res['Дата'] = pd.to_datetime(res["Дата"]).dt.date
            # res = res.round(2)
            # res_min = res_min.round(2)
            # res_max = res_max.round(2)

            # res_g = res_g.round(2)
            # res_min_g = res_min_g.round(2)
            # res_max_g = res_max_g.round(2)

            # print(res_max)

            self.ui.tableWidget.clear()
            self.ui.tableWidget.setRowCount(0)


            if res.empty != True and res_g.empty != True:
                self.ui.tableWidget.setColumnCount(7)
                N = 7
                rows = (len(res.axes[0]))
                columns = (len(res.axes[1]))
                self.ui.tableWidget.setHorizontalHeaderLabels(['Дата', 'Минимальная Temperature Air, °C', 'Средняя Temperature Air, °C', 
                                                            'Максимальная Temperature Air, °C' , 'Минимальная Temperature Ground, °C', 
                                                           'Средняя Temperature Ground, °C', 'Максимальная Temperature Ground, °C'])
            
            elif res_g.empty == True and res.empty != True:
                self.ui.tableWidget.setColumnCount(N)
                rows = (len(res.axes[0]))
                columns = (len(res.axes[1]))
                self.ui.tableWidget.setHorizontalHeaderLabels(['Дата', 'Минимальная Temperature Air, °C', 'Средняя Temperature Air, °C', 
                                                            'Максимальная Temperature Air, °C'])
            elif res.empty == True and res_g.empty != True:
                self.ui.tableWidget.setColumnCount(N)
                rows = (len(res_g.axes[0]))
                columns = (len(res_g.axes[1]))
                self.ui.tableWidget.setHorizontalHeaderLabels(['Дата', 'Минимальная Temperature Ground, °C', 
                                                           'Средняя Temperature Ground, °C', 'Максимальная Temperature Ground, °C'])
            else: 
                return


            # Отображение данных
            for row in range(rows):
                self.ui.tableWidget.setRowCount(row+1)
                if res.empty != True and res_g.empty != True:
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str((res[res.columns[0]].iloc[row]))))
                    self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(res_min[res_min.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(res[res.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(res_max[res_max.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(str(res_min_g[res_min_g.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 5, QTableWidgetItem(str(res_g[res_g.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 6, QTableWidgetItem(str(res_max_g[res_max_g.columns[1]].iloc[row])))
                elif res_g.empty == True and res.empty != True:
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str((res[res.columns[0]].iloc[row]))))
                    self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(res_min[res_min.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(res[res.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(res_max[res_max.columns[1]].iloc[row])))
                elif res.empty == True and res_g.empty != True:
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str((res_g[res_g.columns[0]].iloc[row]))))
                    self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(str(res_min_g[res_min_g.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(str(res_g[res_g.columns[1]].iloc[row])))
                    self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(str(res_max_g[res_max_g.columns[1]].iloc[row])))
                if row%2 ==1:
                    for i in range(N):
                        self.ui.tableWidget.item(row, i).setBackground(QtGui.QColor(202, 204, 206))
        except:
            pass


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