# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 691)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.date_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.date_checkBox.setMinimumSize(QtCore.QSize(20, 20))
        self.date_checkBox.setMaximumSize(QtCore.QSize(20, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.date_checkBox.setFont(font)
        self.date_checkBox.setText("")
        self.date_checkBox.setObjectName("date_checkBox")
        self.horizontalLayout.addWidget(self.date_checkBox)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.dateTimeEdit_min = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_min.setMinimumSize(QtCore.QSize(150, 0))
        self.dateTimeEdit_min.setMaximumSize(QtCore.QSize(150, 16777215))
        self.dateTimeEdit_min.setCalendarPopup(True)
        self.dateTimeEdit_min.setObjectName("dateTimeEdit_min")
        self.horizontalLayout.addWidget(self.dateTimeEdit_min)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dateTimeEdit_max = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_max.setMinimumSize(QtCore.QSize(150, 0))
        self.dateTimeEdit_max.setMaximumSize(QtCore.QSize(150, 16777215))
        self.dateTimeEdit_max.setDate(QtCore.QDate(2000, 1, 2))
        self.dateTimeEdit_max.setCalendarPopup(True)
        self.dateTimeEdit_max.setObjectName("dateTimeEdit_max")
        self.horizontalLayout.addWidget(self.dateTimeEdit_max)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.sensor_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.sensor_checkBox.setMinimumSize(QtCore.QSize(20, 20))
        self.sensor_checkBox.setMaximumSize(QtCore.QSize(20, 20))
        self.sensor_checkBox.setText("")
        self.sensor_checkBox.setObjectName("sensor_checkBox")
        self.horizontalLayout.addWidget(self.sensor_checkBox)
        self.sensors_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.sensors_comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.sensors_comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.sensors_comboBox.setObjectName("sensors_comboBox")
        self.horizontalLayout.addWidget(self.sensors_comboBox)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.type_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.type_checkBox.setMinimumSize(QtCore.QSize(20, 20))
        self.type_checkBox.setMaximumSize(QtCore.QSize(20, 20))
        self.type_checkBox.setText("")
        self.type_checkBox.setObjectName("type_checkBox")
        self.horizontalLayout.addWidget(self.type_checkBox)
        self.type_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.type_comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.type_comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.type_comboBox.setObjectName("type_comboBox")
        self.horizontalLayout.addWidget(self.type_comboBox)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout.addWidget(self.line_4)
        self.true_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.true_checkBox.setMinimumSize(QtCore.QSize(20, 20))
        self.true_checkBox.setMaximumSize(QtCore.QSize(20, 20))
        self.true_checkBox.setText("")
        self.true_checkBox.setObjectName("true_checkBox")
        self.horizontalLayout.addWidget(self.true_checkBox)
        self.true_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.true_comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.true_comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.true_comboBox.setObjectName("true_comboBox")
        self.horizontalLayout.addWidget(self.true_comboBox)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout.addWidget(self.line_5)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menu_3)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menu_3)
        self.menu_5.setObjectName("menu_5")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.load_action = QtWidgets.QAction(MainWindow)
        self.load_action.setObjectName("load_action")
        self.save_action = QtWidgets.QAction(MainWindow)
        self.save_action.setObjectName("save_action")
        self.show_senssors_action = QtWidgets.QAction(MainWindow)
        self.show_senssors_action.setObjectName("show_senssors_action")
        self.show_map_sensors_action = QtWidgets.QAction(MainWindow)
        self.show_map_sensors_action.setObjectName("show_map_sensors_action")
        self.add_sensor_action = QtWidgets.QAction(MainWindow)
        self.add_sensor_action.setObjectName("add_sensor_action")
        self.add_data_to_DB_action = QtWidgets.QAction(MainWindow)
        self.add_data_to_DB_action.setObjectName("add_data_to_DB_action")
        self.max_action = QtWidgets.QAction(MainWindow)
        self.max_action.setObjectName("max_action")
        self.min_action = QtWidgets.QAction(MainWindow)
        self.min_action.setObjectName("min_action")
        self.mean_action = QtWidgets.QAction(MainWindow)
        self.mean_action.setObjectName("mean_action")
        self.plot_action = QtWidgets.QAction(MainWindow)
        self.plot_action.setObjectName("plot_action")
        self.day_action = QtWidgets.QAction(MainWindow)
        self.day_action.setObjectName("day_action")
        self.week_action = QtWidgets.QAction(MainWindow)
        self.week_action.setObjectName("week_action")
        self.month_action = QtWidgets.QAction(MainWindow)
        self.month_action.setObjectName("month_action")
        self.menu.addAction(self.load_action)
        self.menu.addAction(self.save_action)
        self.menu_2.addAction(self.show_senssors_action)
        self.menu_2.addAction(self.show_map_sensors_action)
        self.menu_2.addAction(self.add_sensor_action)
        self.menu_4.addAction(self.max_action)
        self.menu_4.addAction(self.min_action)
        self.menu_4.addAction(self.mean_action)
        self.menu_5.addAction(self.day_action)
        self.menu_5.addAction(self.week_action)
        self.menu_5.addAction(self.month_action)
        self.menu_3.addAction(self.add_data_to_DB_action)
        self.menu_3.addAction(self.menu_4.menuAction())
        self.menu_3.addAction(self.plot_action)
        self.menu_3.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GeoApp"))
        self.pushButton.setText(_translate("MainWindow", "Обновить"))
        self.label_2.setText(_translate("MainWindow", "С:"))
        self.label.setText(_translate("MainWindow", "До:"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainWindow", "Датчики"))
        self.menu_3.setTitle(_translate("MainWindow", "Данные"))
        self.menu_4.setTitle(_translate("MainWindow", "Вычислить"))
        self.menu_5.setTitle(_translate("MainWindow", "Срочные"))
        self.load_action.setText(_translate("MainWindow", "Загрузить"))
        self.save_action.setText(_translate("MainWindow", "Сохранить"))
        self.show_senssors_action.setText(_translate("MainWindow", "Показать"))
        self.show_map_sensors_action.setText(_translate("MainWindow", "Карта"))
        self.add_sensor_action.setText(_translate("MainWindow", "Добавить"))
        self.add_data_to_DB_action.setText(_translate("MainWindow", "Загрузить"))
        self.max_action.setText(_translate("MainWindow", "Максимум"))
        self.min_action.setText(_translate("MainWindow", "Минимум"))
        self.mean_action.setText(_translate("MainWindow", "Среднее"))
        self.plot_action.setText(_translate("MainWindow", "График"))
        self.day_action.setText(_translate("MainWindow", "День"))
        self.week_action.setText(_translate("MainWindow", "Неделя"))
        self.month_action.setText(_translate("MainWindow", "Месяц"))