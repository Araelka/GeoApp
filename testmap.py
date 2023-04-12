from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from folium.plugins import Draw, MousePosition, MarkerCluster
import folium, io, sys, json


if __name__ == '__main__': 
    
    app = QtWidgets.QApplication(sys.argv)

    m = folium.Map(location=[55.8527, 37.5689], zoom_start=13)

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

    # MousePosition().add_to(m)

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

   #  Lt = folium.LatLngPopup()
   #  m.add_child(Lt)

   #  marker_cluster = MarkerCluster().add_to(m)
   #  folium.Marker(location=[54.65464, 53.6547]).add_to(m)

   

   #  folium.ClickForMarker('<b>Lat:</b> ${lat}<br /><b>Lon:</b> ${lng}').add_to(m)
   #  m.add_child(a)
    data = io.BytesIO()
    m.save(data, close_file=False)


    class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
       def javaScriptConsoleMessage(self, level, msg, line, sourceID):
          coords_dict = json.loads(msg)
          coordsE = coords_dict['geometry']['coordinates'][0]
          coordsN = coords_dict['geometry']['coordinates'][1]
          print(coordsN, coordsE)



    view = QtWebEngineWidgets.QWebEngineView()
    page = WebEnginePage(view)
    view.setPage(page)
    view.setHtml(data.getvalue().decode())
    view.show()
    sys.exit(app.exec_())
