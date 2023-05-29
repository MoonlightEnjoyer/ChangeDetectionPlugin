import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from UserInterface.coordinates import Coordinates

class ProductInfo():

    def __init__(self, latitude, longitude, year, max_cloud_cover = 100.0):
        self.coordinates = Coordinates(latitude, longitude)
        self.year = year
        self.max_cloud_cover = max_cloud_cover