import os
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt import QtWidgets
import sys
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from ImageDownloadBlock.product import Product
from UserInterface.results_viewer_dialog import ResultsViewerDialog
from UserInterface.product_download_dialog import ProductDownloadDialog
from ApiInteractionBlock.api_requests import ApiRequests
from UserInterface.model_train_dialog import ModelTrainDialog
from UserInterface.map_dialog_base import MapDialogBase
from SegmentationBlock.segmentation import Segmentation
from ImageDownloadBlock.products_downloader import ProductsDownloader
from ChangemapBlock.changemap_builder import ChangemapBuilder
from ImageSelectorBlock.image_selector import ImageSelector
from ImageProcessingBlock.image_preprocessor import ImagePreprocessor
import os.path
from os import path
from threading import Thread
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_files/change_detection_dialog.ui'))

class ChangeDetectionPluginDialog(QtWidgets.QDialog, MapDialogBase, FORM_CLASS):
    def __init__(self, parent=None):
        super(ChangeDetectionPluginDialog, self).__init__(parent)
        self.setupUi(self)
        self.loadMap()
        self.setMouseTracking(True)
        self.progress_bar.setVisible(False)
        self.results_viewer_button.clicked.connect(self.open_results_viewer_dialog)
        self.download_button.clicked.connect(self.open_product_download_dialog)
        self.train_net_button.clicked.connect(self.open_train_dialog)
        self.apply_coords.clicked.connect(self.comparison_pipeline)
        self.dialogs = list() 

    def open_train_dialog(self):
        dialog = ModelTrainDialog()
        self.dialogs.append(dialog)
        dialog.show()

    def open_results_viewer_dialog(self):
        email, password = self.get_user_data()
        api = ApiRequests(email, password)
        api.token_request()

        products_data = api.images_data_request(self.latitude, self.longitude, 2022)['features']

        products = self.get_products_data(products_data)

        if len(products) == 0:
            return

        for product in products:
            dialog = ResultsViewerDialog(product)
            self.dialogs.append(dialog)
            dialog.show()

    def open_product_download_dialog(self):
        dialog = ProductDownloadDialog()
        self.dialogs.append(dialog)
        dialog.show()

    def get_products_data(self, raw_products):
        products = []
        for raw_product in raw_products:
            product = Product(raw_product)
            if not any((p.relative_orbit==product.relative_orbit and p.tile_id==product.tile_id and p.date==product.date) for p in products):
                products.append(product)
        return products
    
    def comparison_pipeline(self):
        thread = Thread(target=self.comparison_pipeline_thread)
        thread.start()

    def comparison_pipeline_thread(self):
        self.apply_coords.setEnabled(False)
        self.start_year.setEnabled(False)
        self.completion_year.setEnabled(False)
        self.cloud_cover.setEnabled(False)

        download_directory = "D:/Study shit/Diploma/sentinel_products/"
        
        if not path.isdir(download_directory):
            os.mkdir(download_directory)
        
        email, password = self.get_user_data()
        api = ApiRequests(email, password)
        api.token_request()
        
        image_selector = ImageSelector()

        products_to_download = image_selector.select_products(self.latitude, self.longitude, int(self.start_year.currentText()), int(self.completion_year.currentText()), self.cloud_cover.value(), api)
        
        progress = 0
        products_number = len(products_to_download)

        downloaded_images = []

        self.progress_bar.setVisible(True)
        self.info_label.setText("Выполняется загрузка продуктов. Загружено продуктов: %d из %d" % (progress, products_number))

        downloader = ProductsDownloader(download_directory)

        for product in products_to_download:
            bands_path = downloader.download_product(product, api)
            if downloaded_images.count(bands_path) == 0:
                downloaded_images.append(bands_path)
            progress += 1
            self.info_label.setText("Выполняется загрузка продуктов. Загружено продуктов: %d из %d" % (progress, products_number))

        self.info_label.setText("Загрузка продуктов завершена")
        seg = Segmentation()
        image_src = []
        progress = 0
        images_number = len(downloaded_images)
        self.info_label.setText("Выполняется сегментация изображений. Изображений сегментировано: %d из %d" % (progress, images_number))
        for image in downloaded_images:            
            image_preprocesor =  ImagePreprocessor()
            image_preprocesor.remove_clouds(image)
            image_src.append(image + "segmentation_result.png")
            if not path.isdir(image):
                os.mkdir(image)
            seg.perform_segmentation(image + "clouds_removed.jp2", image, self.progress_bar)
            progress += 1
            self.info_label.setText("Выполняется сегментация изображений. Изображений сегментировано: %d из %d" % (progress, images_number))
        change_builder = ChangemapBuilder()
        progress = 0
        changemaps_number = int(len(downloaded_images) / 2)
        self.info_label.setText("Выполняется построение карты изменений. Карт построено: %d из %d" % (progress, changemaps_number))
        for i in range(1, len(downloaded_images), 2):
            change_builder.build_changemap(downloaded_images[i] + "clouds_removed.jp2", image_src[i - 1], image_src[i], downloaded_images[i])
            progress += 1
            self.info_label.setText("Выполняется построение карты изменений. Карт построено: %d из %d" % (progress, changemaps_number))

        self.progress_bar.setVisible(False)
        self.apply_coords.setEnabled(True)
        self.start_year.setEnabled(True)
        self.completion_year.setEnabled(True)
        self.cloud_cover.setEnabled(True)