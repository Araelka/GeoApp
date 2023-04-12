from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QWidget,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)
from folium.plugins import Draw, MousePosition, MarkerCluster
import folium, io, sys, json


class Map(QDialog):
    def __init__(self, parent=None, coords=[]):
        super(Map, self).__init__(parent) 
        self.coords = coords


        self.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.centralwidget = QtWidgets.QWidget(self)
        self.view = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.verticalLayout.addWidget(self.view)

        self.page = self.WebEnginePage(self.view)

        self.date = self.initmap()

        self.view.setPage(self.page)
        self.view.setHtml(self.date.getvalue().decode())

        # self.view.show()



    def initmap(self):
        m = folium.Map(location=[51.554021, 83.100586], zoom_start=10)

        # layout = QVBoxLayout()
        # self.setLayout(layout)

        # draw = Draw(show_geometry_on_click= True,
        # draw_options={
        #     'polyline':False,
        #     'rectangle':True,
        #     'polygon':False,
        #     'circle':False,
        #     'marker':True,
        #     'circlemarker':False},
        # edit_options={'edit':False})
        
        # Lt = folium.LatLngPopup()
        # m.add_child(Lt)

        # m.add_child(draw)

        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

        folium.ClickForMarker('<b>Новый датчик</b><br /> <b>N/S:</b> ${lat}<br /><b>E/W:</b> ${lng}').add_to(m)


        MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Координаты:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(m)

        # Добавление датчиков
        for i in self.coords:
            folium.Marker(location=[i[1], i[2]], popup='<b>'+str(i[0])+'</b><br /> <b>N/S:</b>'+ str(i[1])+'<br /><b>E/W:</b>' + str(i[2])).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        return data

        # view.show()
        # layout.addWidget(view)

    class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
        def javaScriptConsoleMessage(self, level, msg, line, sourceID):
            coords_dict = json.loads(msg)
            coordsE = coords_dict['geometry']['coordinates'][0]
            coordsN = coords_dict['geometry']['coordinates'][1]
            coords = [coordsN, coordsE]
            print(coords)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    application = Map()
    application.show()
    sys.exit(app.exec_())
