import os
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QDate
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt import QtWidgets
from datetime import date
from threading import Thread
import sys
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from ImageDownloadBlock.products_downloader import ProductsDownloader
from ApiInteractionBlock.api_requests import ApiRequests
from UserInterface.map_dialog_base import MapDialogBase
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_files/product_download_dialog.ui'))

class ProductDownloadDialog(QtWidgets.QDialog, MapDialogBase, FORM_CLASS):
    def __init__(self, parent=None):
        super(ProductDownloadDialog, self).__init__(parent)
        
        self.setupUi(self)
        self.loadMap()
        self.setMouseTracking(True)
        self.downloadButton.clicked.connect(self.download_products)
        self.completion_date.setMaximumDate(QDate(date.today().year, date.today().month, date.today().day))
        self.start_date.setMaximumDate(QDate(date.today().year, date.today().month, date.today().day))
        self.text_scroll_area.setWidget(self.info_label)

    def select_download_directory(self):
        return str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def download_products(self):
        thread = Thread(target=self.download_products_thread)
        thread.start()

    def download_products_thread(self):
        self.downloadButton.setEnabled(False)
        self.clouds_cover_selector.setEnabled(False)
        self.start_date.setEnabled(False)
        self.completion_date.setEnabled(False)
        
        email, password = self.get_user_data()
        api = ApiRequests(email, password)
        api.token_request()
        downloader = ProductsDownloader(self.select_download_directory() + "/")
        products = api.images_data_request(self.latitude, self.longitude, f'{self.start_date.date().year()}-{self.start_date.date().month():02d}-{self.start_date.date().day():02d}', f'{self.completion_date.date().year()}-{self.completion_date.date().month():02d}-{self.completion_date.date().day():02d}', self.clouds_cover_selector.value())
        progress = 0
        products_number = len(products)

        self.info_label.setText("Количество продуктов, которые должны быть загружены: %d" % products_number)

        for raw_product in products:
            product = Product(raw_product)
            downloader.download_product_full(product, api)
            progress += 1
            self.progressBar.setValue(int((progress / products_number) * 100))

        self.downloadButton.setEnabled(True)
        self.clouds_cover_selector.setEnabled(True)
        self.start_date.setEnabled(True)
        self.completion_date.setEnabled(True)