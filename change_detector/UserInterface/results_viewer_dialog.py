import os
import cv2
import sys
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from threading import Thread
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from DataExportBlock.data_export import DataExport
from ImageProcessingBlock.results_analyser import ResultsAnalyser
import json
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_files/results_viewer_dialog.ui'))

class ResultsViewerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, product_old, product_new,  parent=None):
        self.product_old = product_old
        self.product_new = product_new
        super(ResultsViewerDialog, self).__init__(parent)

        self.setupUi(self)
        self.image_type.activated.connect(self.load_image)
        self.year_combo_box.activated.connect(self.load_image)
        self.export_button.clicked.connect(self.export_data_thread)
        self.change_size_button.clicked.connect(self.change_size)
        self.setMouseTracking(True)
        self.scroll_area.setMouseTracking(True)
        self.image_label.setMouseTracking(True)
        self.image_label.setVisible(False)
        self.scroll_area.setVisible(False)
        self.progress_bar.setVisible(False)
        self.pixmap = QPixmap()
        self.current_image = ''
        self.temp_path = ''
        self.size = int(10980 * self.image_size_selector.value() / 100)
        self.scroll_area.setWidget(self.image_label)
        self.old_image = None
        self.new_image = None
        self.text_scroll_area.setWidget(self.info_label)
        self.year_combo_box.addItem(product_new.date)
        self.year_combo_box.addItem(product_old.date)

        self.load_image()

    def load_image(self):
        self.image_label.setVisible(True)
        self.scroll_area.setVisible(True)
        image_path = fr"D:\Study shit\Diploma\sentinel_products/" + self.product_new.tile_id + '/' + self.product_new.relative_orbit + '/' + self.year_combo_box.currentText() + '/'
        if self.image_type.currentText() == 'Карта изменений':
            image_path += 'changemap.png'
        if self.image_type.currentText() == 'Сегментированное изображение':
            image_path += 'visualized_segmentation.png'
        if self.image_type.currentText() == 'Оригинальное изображение':
            image_path += 'clouds_removed.jp2'
        
        self.current_image = image_path
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (self.size, self.size), interpolation = cv2.INTER_AREA)
        self.temp_path = image_path[:-4] + '_temp.png'
        cv2.imwrite(self.temp_path, resized_image)
        self.pixmap = QPixmap(self.temp_path)
        self.image_label.setPixmap(self.pixmap)

        self.old_image = cv2.imread(fr'D:\Study shit\Diploma\sentinel_products\{self.product_old.tile_id}\{self.product_old.relative_orbit}\{self.product_old.date}\segmentation_result.png', cv2.IMREAD_UNCHANGED)
        self.new_image = cv2.imread(fr'D:\Study shit\Diploma\sentinel_products\{self.product_new.tile_id}\{self.product_new.relative_orbit}\{self.product_new.date}\segmentation_result.png', cv2.IMREAD_UNCHANGED)
        self.old_image = cv2.resize(self.old_image, (self.size, self.size), interpolation = cv2.INTER_AREA)
        self.new_image = cv2.resize(self.new_image, (self.size, self.size), interpolation = cv2.INTER_AREA)

    def change_size(self):
        thread = Thread(target=self.change_size_thread)
        thread.start()

    def change_size_thread(self):
        self.size = int(10980 * self.image_size_selector.value() / 100)
        image = cv2.imread(self.current_image)
        resized_image = cv2.resize(image, (self.size, self.size), interpolation = cv2.INTER_AREA)
        cv2.imwrite(self.temp_path, resized_image)
        self.pixmap = QPixmap(self.temp_path)
        self.image_label.setPixmap(self.pixmap)

        self.old_image = cv2.imread(fr'D:\Study shit\Diploma\sentinel_products\{self.product_old.tile_id}\{self.product_old.relative_orbit}\{self.product_old.date}\segmentation_result.png', cv2.IMREAD_UNCHANGED)
        self.new_image = cv2.imread(fr'D:\Study shit\Diploma\sentinel_products\{self.product_new.tile_id}\{self.product_new.relative_orbit}\{self.product_new.date}\segmentation_result.png', cv2.IMREAD_UNCHANGED)
        self.old_image = cv2.resize(self.old_image, (self.size, self.size), interpolation = cv2.INTER_AREA)
        self.new_image = cv2.resize(self.new_image, (self.size, self.size), interpolation = cv2.INTER_AREA)

    def export_data(self):
        thread = Thread(target=self.export_data_thread)
        thread.start()

    def export_data_thread(self):
        download_dir = json.load(open(fr"{SCRIPT_DIR}\configuration.txt"))['download_directory'] + fr'{self.product_old.tile_id}\{self.product_old.relative_orbit}' + '\\'
        resultsAnalyzer = ResultsAnalyser()
        coordinates = resultsAnalyzer.get_changed_areas_coords(fr"{download_dir}\2022\\")
        dataExport = DataExport()
        self.progress_bar.setVisible(True)

        seg_result_old = fr'D:\Study shit\Diploma\sentinel_products\{self.product_old.tile_id}\{self.product_old.relative_orbit}\{self.product_old.date}\segmentation_result.png'
        seg_result_new = fr'D:\Study shit\Diploma\sentinel_products\{self.product_new.tile_id}\{self.product_new.relative_orbit}\{self.product_new.date}\segmentation_result.png'

        if self.data_format.currentText() == "JSON":
            dataExport.export_json(coordinates, seg_result_old, seg_result_new, fr'D:\Study shit\Diploma\sentinel_products\{self.product_new.tile_id}\{self.product_new.relative_orbit}\{self.product_new.date}\exported_data.json', self.progress_bar)
        if self.data_format.currentText() == "AVRO":
            dataExport.export_avro(coordinates, seg_result_old, seg_result_new, fr'D:\Study shit\Diploma\sentinel_products\{self.product_new.tile_id}\{self.product_new.relative_orbit}\{self.product_new.date}\exported_data.avro', self.progress_bar)
        if self.data_format.currentText() == "CSV":
            dataExport.export_csv(coordinates, seg_result_old, seg_result_new, fr'D:\Study shit\Diploma\sentinel_products\{self.product_new.tile_id}\{self.product_new.relative_orbit}\{self.product_new.date}\exported_data.csv', self.progress_bar)
        if self.data_format.currentText() == "POSTGRESQL":
            dataExport.export_sql(coordinates, seg_result_old, seg_result_new, "dbname=%s user=%s password=%s host=%s port=%s" % ("postgres", "postgres", "lartem2001", "localhost", "5432"), self.progress_bar)

        self.progress_bar.setVisible(False)

    def get_class_name(self, value):
        if value == 0:
            return 'постройки'
        elif value == 1:
            return 'вода'
        elif value == 2:
            return 'поле'
        elif value == 3:
            return 'лес'
        elif value == 4:
            return 'поле'
        elif value == 5:
            return 'облака'
        elif value == 6:
            return 'пустая область'

    def mouseMoveEvent(self, event):
        x = event.x() - 10
        y = event.y() - 10
        if (x < 0 or y < 0 or x >= 549 or y >= 549):
            return

        scaled_x = x + self.scroll_area.verticalScrollBar().value()
        scaled_y = y + self.scroll_area.horizontalScrollBar().value()
        self.info_label.setText(f'{y}, {x} : {self.get_class_name(self.old_image[scaled_y][scaled_x])} -> {self.get_class_name(self.new_image[scaled_y][scaled_x])}')