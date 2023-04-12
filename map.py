from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import *
from folium.plugins import Draw, MousePosition
import folium, io, sys, json


class Map(QtWebEngineWidgets.QWebEngineView):
    def __init__(self):
        super().__init__()      
        self.date = self.initmap()
        self.information_window = Map()

    def initmap(self):
        m = folium.Map(location=[55.8527, 37.5689], zoom_start=13)

        # layout = QVBoxLayout()
        # self.setLayout(layout)

        draw = Draw(show_geometry_on_click= True,
        draw_options={
            'polyline':False,
            'rectangle':True,
            'polygon':False,
            'circle':False,
            'marker':True,
            'circlemarker':False},
        edit_options={'edit':False})
        
        m.add_child(draw)

        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

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
          print(coordsN, coordsE)

    def showmap(self):
        page = self.WebEnginePage(self)
        self.setPage(page)
        self.setHtml(self.date.getvalue().decode())
        # self.information_window.show()
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    application = Map()
    # view = QtWebEngineWidgets.QWebEngineView()
    # page = application.WebEnginePage(application)
    # application.setPage(page)
    # application.setHtml(application.date.getvalue().decode())
    # application.show()
    application.showmap()
    # application.show()
    sys.exit(app.exec_())
