from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

class MapDialogBase():
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.work_directory = ''
        
    def loadMap(self):
        photoPath=fr'C:\Users\Artem\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\change_detector\UserInterface\resources\belarus-map-small.png'
        self.map_label.setPixmap(QPixmap(photoPath))

    def get_coords(self, x, y):
        minsk_lat = 53.9000468 # Minsk latitude
        minsk_lon = 27.551224 # Minsk longitude
        mog_lon = 30.330671 # Mogilev longitude
        minsk_x = 275 #Minsk x position
        minsk_y = 230 # Minsk y position
        mog_x = 443 # Mogilev x position
        pol_lat = 55.486796 # Polotsk latitude
        pol_y = 68 # Polotsk y position
        (lat_coef, lon_coef) = (abs(minsk_lat - pol_lat) / abs(minsk_y - pol_y), abs(minsk_lon - mog_lon) / abs(minsk_x - mog_x))
        return  (minsk_lat + (minsk_y - y) * lat_coef, minsk_lon + (x - minsk_x) * lon_coef)
    
    def mouseReleaseEvent(self, event):
        (self.latitude, self.longitude) = self.get_coords(event.x() - 120, event.y() - 50)