import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from DatasetBuilderBlock.data_preparation import DataPreparation
from DatasetBuilderBlock.dataset_builder import DatasetBuilder
from ModelTrainBlock.model_train import ModelTrain

class ModelTrainManager:
    def train_pipeline(self, info_label):
        data_preparation = DataPreparation()
        dataset_builder = DatasetBuilder("C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\", "C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\bands\\")
        
        data_preparation.mark_masks_color("C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\bands\\", "C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\bands\\")
        dataset_builder.build_dataset()

        model_train = ModelTrain()
        model_train.train(info_label)