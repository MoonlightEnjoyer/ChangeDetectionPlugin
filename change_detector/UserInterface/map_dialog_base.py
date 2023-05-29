from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
import cv2
import json
import os

class MapDialogBase():
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.marker_x = -1
        self.marker_y = -1
        self.work_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cv2.imwrite(fr'{self.work_directory}\UserInterface\resources\map_temp.png', cv2.imread(fr'{self.work_directory}\UserInterface\resources\belarus_map_source.png'))
        
    def get_user_data(self):
        config = json.load(open(fr"{self.work_directory}\configuration.txt"))
        return config['email'], config['password']

    def loadMap(self):
        photoPath=fr'{self.work_directory}\UserInterface\resources\map_temp.png'
        self.map_label.setPixmap(QPixmap(photoPath))

    def get_coords(self, x, y):
        minsk_lat = 53.9000468 # Minsk latitude
        minsk_lon = 27.551224 # Minsk longitude
        mog_lon = 30.330671 # Mogilev longitude
        minsk_x = 275 #Minsk x position
        minsk_y = 290 # Minsk y position
        mog_x = 443 # Mogilev x position
        pol_lat = 55.486796 # Polotsk latitude
        pol_y = 128 # Polotsk y position
        (lat_coef, lon_coef) = (abs(minsk_lat - pol_lat) / abs(minsk_y - pol_y), abs(minsk_lon - mog_lon) / abs(minsk_x - mog_x))
        return  (minsk_lat + (minsk_y - y) * lat_coef, minsk_lon + (x - minsk_x) * lon_coef)
    
    def mouseReleaseEvent(self, event):
        x = event.x() - 20
        y = event.y() - 20

        (self.latitude, self.longitude) = self.get_coords(x, y)
        map = cv2.imread(fr'{self.work_directory}\UserInterface\resources\belarus_map_source.png')
        marker = cv2.imread(fr'{self.work_directory}\UserInterface\resources\marker.png')

        rows, cols, _ = marker.shape

        y -= (rows - 5)
        x -= int(cols / 2)

        if y < 0 or x < 0:
            return

        roi = map[y:(rows + y), x:(cols + x) ]
        marker_gray = cv2.cvtColor(marker,cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(marker_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        map_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        marker_fg = cv2.bitwise_and(marker,marker,mask = mask)
        dst = cv2.add(map_bg,marker_fg)
        map[y:(rows + y), x:(cols + x) ] = dst

        cv2.imwrite(fr'{self.work_directory}\UserInterface\resources\map_temp.png', map)

        self.loadMap()

        