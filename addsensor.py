import sys
from  GUIaddsensor import Ui_add_sensor_Dialog
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


class AddSensor(QDialog):
    # Инициализация диалогового окна для добавления датчика
    def __init__(self, parent=None, ls=[], coords=[]):
        super(AddSensor, self).__init__(parent)
        self.ui = Ui_add_sensor_Dialog()
        self.ui.setupUi(self)
        self.ui.cancel_pushButton.clicked.connect(self.close)
        self.ui.add_pushButton.clicked.connect(self.saveValue)
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.map_pushButton.clicked.connect(self.mapshow)
        self.coords = coords
        for i in ls:
            self.ui.type_comboBox.addItem(ls[i], i)

    # закрытие окна по кнопке "Отмена"
    def close(self):
        return super().close()
    

    # считывание данных из формы и возвращение результатов
    def saveValue(self):
        try:
            name = self.ui.name_textEdit.toPlainText()
            serial_number = int(self.ui.serial_number_textEdit.toPlainText())
            type_sens = int(self.ui.type_comboBox.currentData())
            N_S = float(self.ui.N_S_textEdit.toPlainText())
            E_W = float(self.ui.E_W_textEdit.toPlainText())
            date = self.ui.dateEdit.date().toString('dd-MM-yyyy')
            location = self.ui.location_textEdit.toPlainText()
            sens_value = [name, serial_number, type_sens, N_S, E_W, date, location]
            self.close()
            return sens_value
        except:
            sens_value = []
            return sens_value

    # Открытие карты
    def mapshow(self):
        new_map = map.Map(coords = self.coords)
        new_map.exec_()
        try:
            coords = new_map.page.returncoords()
            self.ui.E_W_textEdit.setText(str(coords[0]))
            self.ui.N_S_textEdit.setText(str(coords[1]))
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    application = AddSensor()
    application.show()
    sys.exit(app.exec_())
