import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)
from ImageDownloadBlock.product import Product
from UserInterface.product_info import ProductInfo
from UserInterface.coordinates import Coordinates
from ApiInteractionBlock.api_requests import ApiRequests
from multipledispatch import dispatch

class ImageSelector():
    def request_images_data(self, product_info_early, product_info_late, api):
        products_early = api.images_data_request(product_info_early.coordinates.latitude, product_info_early.coordinates.longitude, product_info_early.year, product_info_early.max_cloud_cover)['features']
        products_late = api.images_data_request(product_info_late.coordinates.latitude, product_info_late.coordinates.longitude, product_info_late.year, product_info_late.max_cloud_cover)['features']
        return (products_early, products_late)

    @dispatch(float, float, int, int, float, ApiRequests)
    def select_products(self, latitude, longitude, start_year, completion_year, max_cloud_cover, api):
        product_info_early = ProductInfo(Coordinates(latitude, longitude), start_year, max_cloud_cover)
        product_info_late = ProductInfo(Coordinates(latitude, longitude), completion_year, max_cloud_cover)
        products_early, products_late = self.request_images_data(product_info_early, product_info_late, api)
        return self.select_products(products_early, products_late)

    @dispatch(list, list)
    def select_products(self, products_early, products_late):
        early_products_download = {}
        late_products_download = {}

        for raw_product in products_early:
            product = Product(raw_product)

            if not (product.tile_id, product.relative_orbit) in early_products_download:
                early_products_download[(product.tile_id, product.relative_orbit)] = []

            early_products_download[(product.tile_id, product.relative_orbit)].append(product)

        for raw_product in products_late:
            product = Product(raw_product)

            if not (product.tile_id, product.relative_orbit) in late_products_download:
                late_products_download[(product.tile_id, product.relative_orbit)] = []

            late_products_download[(product.tile_id, product.relative_orbit)].append(product)

        for key, group in early_products_download.items():
            early_products_download[key] = sorted(group, key = lambda x: x.clouds)[:2]

        for key, group in late_products_download.items():
            late_products_download[key] = sorted(group, key = lambda x: x.clouds)[:2]
        
        products_to_download = []
        for key, _ in early_products_download.items():
            if key in late_products_download:
                for p in early_products_download[key]:
                    products_to_download.append(p)
                for p in late_products_download[key]:
                    products_to_download.append(p)
        
        return products_to_download