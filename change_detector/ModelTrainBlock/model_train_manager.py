import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from DatasetBuilderBlock.dataset_builder import DatasetBuilder
from ModelTrainBlock.model_train import ModelTrain

class ModelTrainManager:
    def train_pipeline(self, info_label):
        dataset_builder = DatasetBuilder(fr"{SCRIPT_DIR}\\", fr"{SCRIPT_DIR}\bands\\")
        dataset_builder.build_dataset()
        model_train = ModelTrain()
        model_train.train(info_label)