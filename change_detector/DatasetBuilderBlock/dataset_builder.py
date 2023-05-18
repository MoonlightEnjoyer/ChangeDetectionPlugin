import os
import cv2
import numpy as np
import sys
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from SegmentationBlock.image_reshaper import ImageReshaper

class DatasetBuilder:
    def __init__(self, dataset_directory, masks_directory):
        self.dataset_directory = dataset_directory
        self.masks_directory = masks_directory

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
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/buildings/')
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/farmland/')
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/forest/')
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/water/')
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/grass/')
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/clouds/')
        os.mkdir(f'{self.dataset_directory}dataset/train/semantic/ignore/')

        os.mkdir(f'{self.dataset_directory}dataset/test/')
        os.mkdir(f'{self.dataset_directory}dataset/test/image/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/buildings/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/farmland/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/forest/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/water/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/grass/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/clouds/')
        os.mkdir(f'{self.dataset_directory}dataset/test/semantic/ignore/')

    def build_dataset(self):
        self.build_dataset_structure()
        self.separate_image_dataset(f'{self.masks_directory}TCI.jp2', f'{self.dataset_directory}dataset/test/image/', f'{self.dataset_directory}dataset/train/image/', '.png')
        self.separate_image_dataset(f'{self.masks_directory}buildings.png', f'{self.dataset_directory}dataset/test/semantic/buildings/', f'{self.dataset_directory}dataset/train/semantic/buildings/', '.png')
        self.separate_image_dataset(f'{self.masks_directory}farmland.png', f'{self.dataset_directory}dataset/test/semantic/farmland/', f'{self.dataset_directory}dataset/train/semantic/farmland/', '.png')
        self.separate_image_dataset(f'{self.masks_directory}forest.png', f'{self.dataset_directory}dataset/test/semantic/forest/', f'{self.dataset_directory}dataset/train/semantic/forest/', '.png')
        self.separate_image_dataset(f'{self.masks_directory}water.png', f'{self.dataset_directory}dataset/test/semantic/water/', f'{self.dataset_directory}dataset/train/semantic/water/', '.png')
        self.separate_image_dataset(f'{self.masks_directory}grass.png', f'{self.dataset_directory}dataset/test/semantic/grass/', f'{self.dataset_directory}dataset/train/semantic/grass/', '.png')
        self.separate_image_dataset(f'{self.masks_directory}clouds.png', f'{self.dataset_directory}dataset/test/semantic/clouds/', f'{self.dataset_directory}dataset/train/semantic/clouds/', '.png')
        self.separate_image_dataset(f'{self.masks_directory}ignore.png', f'{self.dataset_directory}dataset/test/semantic/ignore/', f'{self.dataset_directory}dataset/train/semantic/ignore/', '.png')
        self.remove_ignore()

    def remove_ignore(self):
        for file in os.listdir(f'{self.dataset_directory}dataset/test/semantic/ignore/'):
            temp = cv2.imread(f'{self.dataset_directory}dataset/test/semantic/ignore/{file}', cv2.IMREAD_UNCHANGED)
            if 1 in temp:
                os.remove(f'{self.dataset_directory}dataset/test/image/{file}')
                os.remove(f'{self.dataset_directory}dataset/test/semantic/buildings/{file}')
                os.remove(f'{self.dataset_directory}dataset/test/semantic/farmland/{file}')
                os.remove(f'{self.dataset_directory}dataset/test/semantic/forest/{file}')
                os.remove(f'{self.dataset_directory}dataset/test/semantic/water/{file}')
                os.remove(f'{self.dataset_directory}dataset/test/semantic/grass/{file}')
                os.remove(f'{self.dataset_directory}dataset/test/semantic/clouds/{file}')
                os.remove(f'{self.dataset_directory}dataset/test/semantic/ignore/{file}')

        for file in os.listdir(f'{self.dataset_directory}dataset/train/semantic/ignore/'):
            temp = cv2.imread(f'{self.dataset_directory}dataset/train/semantic/ignore/{file}', cv2.IMREAD_UNCHANGED)
            if 1 in temp:
                os.remove(f'{self.dataset_directory}dataset/train/image/{file}')
                os.remove(f'{self.dataset_directory}dataset/train/semantic/buildings/{file}')
                os.remove(f'{self.dataset_directory}dataset/train/semantic/farmland/{file}')
                os.remove(f'{self.dataset_directory}dataset/train/semantic/forest/{file}')
                os.remove(f'{self.dataset_directory}dataset/train/semantic/water/{file}')
                os.remove(f'{self.dataset_directory}dataset/train/semantic/grass/{file}')
                os.remove(f'{self.dataset_directory}dataset/train/semantic/clouds/{file}')
                os.remove(f'{self.dataset_directory}dataset/train/semantic/ignore/{file}')

        zeros = np.zeros((122, 122), np.uint8)
        ones = np.ones((122, 122), np.uint8)

        for file in range(200):
            cv2.imwrite(f'{self.dataset_directory}dataset/test/image/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/buildings/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/farmland/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/forest/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/water/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/grass/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/clouds/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/test/semantic/ignore/{file}.png', ones)

            cv2.imwrite(f'{self.dataset_directory}dataset/train/image/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/buildings/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/farmland/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/forest/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/water/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/grass/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/clouds/{file}.png', zeros)
            cv2.imwrite(f'{self.dataset_directory}dataset/train/semantic/ignore/{file}.png', ones)