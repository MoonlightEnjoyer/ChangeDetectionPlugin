import os
import cv2
import numpy as np
import sys
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from SegmentationBlock.image_reshaper import ImageReshaper
from DatasetBuilderBlock.data_preparation import DataPreparation

class DatasetBuilder:
    def __init__(self, dataset_directory, masks_directory):
        self.dataset_directory = dataset_directory
        self.masks_directory = masks_directory
        self.semantic_folders = ['buildings', 'farmland', 'forest', 'water', 'grass', 'clouds', 'ignore']

    def separate_image_dataset(self, filename, test, train, format):
        image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        size = 122
        blocks_number = int((10980 * 10980) / (size * size))

        image_reshaper = ImageReshaper()
        blocks = image_reshaper.split(image, size)

        for c in range(int(blocks_number * 0.2)):
            img = blocks[c]
            cv2.imwrite(test + str(c + 200 + 1) + format, img)

        for c in range(int(blocks_number * 0.2), blocks_number):
            img = blocks[c]
            cv2.imwrite(train + str(c - int(blocks_number * 0.2) + 1 + 200) + format, img)

    def build_dataset_structure(self):
        os.mkdir(f'{self.dataset_directory}dataset/')
        os.mkdir(f'{self.dataset_directory}dataset/train/')
        os.mkdir(f'{self.dataset_directory}dataset/train/image/')
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/')
        os.mkdir(f'{self.dataset_directory}dataset/test/')
        os.mkdir(f'{self.dataset_directory}dataset/test/image/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/')

        for folder in self.semantic_folders:
            os.mkdir(f'{self.dataset_directory}dataset/train/semantic/{folder}/')
            os.mkdir(f'{self.dataset_directory}dataset/test/semantic/{folder}/')

    def build_dataset(self):
        data_preparation = DataPreparation()
        data_preparation.mark_masks_color(fr"{SCRIPT_DIR}\bands\\", fr"{SCRIPT_DIR}\bands\\")


        self.build_dataset_structure()
        self.separate_image_dataset(f'{self.masks_directory}TCI.jp2', f'{self.dataset_directory}dataset/test/image/', f'{self.dataset_directory}dataset/train/image/', '.png')
        for folder in self.semantic_folders:
            self.separate_image_dataset(f'{self.masks_directory}{folder}.png', f'{self.dataset_directory}dataset/test/semantic/{folder}/', f'{self.dataset_directory}dataset/train/semantic/{folder}/', '.png')
        
        self.remove_ignore()

    def remove_ignore(self):
        for file in os.listdir(f'{self.dataset_directory}dataset/test/semantic/ignore/'):
            temp = cv2.imread(f'{self.dataset_directory}dataset/test/semantic/ignore/{file}', cv2.IMREAD_UNCHANGED)
            if 1 in temp:
                os.remove(f'{self.dataset_directory}dataset/test/image/{file}')
                for folder in self.semantic_folders:
                    os.remove(f'{self.dataset_directory}dataset/test/semantic/{folder}/{file}')

        for file in os.listdir(f'{self.dataset_directory}dataset/train/semantic/ignore/'):
            temp = cv2.imread(f'{self.dataset_directory}dataset/train/semantic/ignore/{file}', cv2.IMREAD_UNCHANGED)
            if 1 in temp:
                os.remove(f'{self.dataset_directory}dataset/train/image/{file}')
                for folder in self.semantic_folders:
                    os.remove(f'{self.dataset_directory}dataset/train/semantic/{folder}/{file}')

        zeros = np.zeros((122, 122), np.uint8)
        ones = np.ones((122, 122), np.uint8)

        for file in range(200):
            cv2.imwrite(f'{self.dataset_directory}dataset/test/image/{file}.png', zeros)
            for folder in self.semantic_folders:
                cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/{folder}/{file}.png', zeros)

            cv2.imwrite(f'{self.dataset_directory}dataset/train/image/{file}.png', zeros)
            for folder in self.semantic_folders:
                cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/{folder}/{file}.png', zeros)