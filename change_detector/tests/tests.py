import pytest
import json
import os
import sys
import cv2
import numpy as np

# SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")


from ImageDownloadBlock.product import Product
from ImageSelectorBlock.image_selector import ImageSelector
from UserInterface.map_dialog_base import MapDialogBase
from SegmentationBlock.image_reshaper import ImageReshaper


@pytest.fixture
def selected_products():
    return [
        Product('e00b0d65-d847-5cd8-a0bc-0a2b1e2bc79d', '2019', 'T35UNV', 'R136', 17.282791),
        Product('6d1f2c38-4f23-5859-ae3e-28f0b4eadf7f', '2019', 'T35UNV', 'R136', 20.267938),
        Product('4b70164b-bb9d-591c-9a4b-563fa5851119', '2022', 'T35UNV', 'R136', 1.983062),
        Product('3ab693ba-98b4-585c-9624-8a541226d97b', '2022', 'T35UNV', 'R136', 14.263551000000001),
        Product('50c0d90a-4488-54c4-96bb-ace6f5e60fab', '2019', 'T35UNV', 'R093', 2.896988),
        Product('e706ffaa-6136-501d-a857-a556c83a629e', '2019', 'T35UNV', 'R093', 21.208061),
        Product('fb361f0c-8a80-5b1b-bcd5-7ffc1af70475', '2022', 'T35UNV', 'R093', 21.090713),
        Product('839c8eb2-91ef-5a4b-8334-ce97218aa61d', '2022', 'T35UNV', 'R093', 46.28230299999999),
    ]



def test_selected_products(selected_products):
    f = open("C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\tests\\products_early.txt", "r")
    products_early = json.load(f)['features']
    f.close()

    f = open("C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\change_detector\\tests\\products_late.txt", "r")
    products_late = json.load(f)['features']
    f.close()

    selector = ImageSelector()

    assert selector.select_products(products_early, products_late) == selected_products


def test_calculate_coordinates_grodno():
    map_dialog_base = MapDialogBase()
    latitude, longitude = map_dialog_base.get_coords(47, 255)

    d = 0.1

    assert round(abs(53.6777 - latitude), 1) <= d and round(abs(23.8293 - longitude), 1) <= d

def test_calculate_coordinates_gomel():
    map_dialog_base = MapDialogBase()
    latitude, longitude = map_dialog_base.get_coords(493, 370)

    d = 0.1

    assert round(abs(52.4221 - latitude), 1) <= d and round(abs(31.0129 - longitude), 1) <= d

def test_image_reshaper_split_merge():
    image_reshaper = ImageReshaper()
    image = cv2.imread("test_image.jp2")
    size = 122
    blocks = image_reshaper.split(image, size)
    assert len(blocks) == 10980 * 10980 / (122 * 122)

    reassempled_image = image_reshaper.merge(blocks)

    assert np.array_equal(image, reassempled_image)

def test_split_size_less_than_one():
    image_reshaper = ImageReshaper()
    image = cv2.imread("test_image.jp2")
    size = -1
    blocks = image_reshaper.split(image, size)
    assert blocks == None

def test_split_size_greater_than_shape():
    image_reshaper = ImageReshaper()
    image = cv2.imread("test_image.jp2")
    size = 11000
    blocks = image_reshaper.split(image, size)
    assert blocks == None

def test_merge_blocks_is_none():
    image_reshaper = ImageReshaper()
    blocks = image_reshaper.merge(None)
    assert blocks == None

def test_merge_blocks_is_invalid():
    image_reshaper = ImageReshaper()
    image = cv2.imread("test_image.jp2")
    size = 122
    blocks = image_reshaper.split(image, size)

    reassempled_image = image_reshaper.merge(blocks[:10])

    assert reassempled_image == None

