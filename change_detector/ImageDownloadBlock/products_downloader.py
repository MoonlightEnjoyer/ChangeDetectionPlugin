import requests
import os
from zipfile import ZipFile
import shutil
from os import path

class ProductsDownloader():

    def __init__(self, download_directory):
        self.download_directory = download_directory

    def download_product(self, product, api):
        if not path.isdir(self.download_directory + product.tile_id):
            os.mkdir(self.download_directory + product.tile_id)
        if not path.isdir(self.download_directory + product.tile_id + "/" + product.relative_orbit):
            os.mkdir(self.download_directory + product.tile_id + "/" + product.relative_orbit)
        if not path.isdir(self.download_directory + product.tile_id + "/" + product.relative_orbit + "/" + product.date):
            os.mkdir(self.download_directory + product.tile_id + "/" + product.relative_orbit + "/" + product.date)

        local_filename = self.download_directory + product.tile_id + "/" + product.relative_orbit + "/" + product.date + "/" + product.id + ".zip"
        
        try:
            with api.download_request(product) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk) 
        except requests.HTTPError as err:
                try:
                    if err.response.status_code == 401:
                        api.regenerate_token_request()
                        if os.path.isfile(local_filename):
                            os.remove(local_filename)
                        with api.download_request(product) as r:
                            r.raise_for_status()
                            with open(local_filename, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=8192): 
                                    f.write(chunk)
                    else:
                        return None
                except Exception:
                     return None
        except Exception:
            return None
        
        with ZipFile(local_filename, 'r') as zObject:
                    zObject.extractall(path=self.download_directory + product.tile_id + "/" + product.relative_orbit + "/" + product.date + "/")
        
        os.remove(local_filename)

        bands_path = self.download_directory + product.tile_id + "/" + product.relative_orbit + "/" + product.date + "/"
        for dir in os.listdir(bands_path):
            if os.path.isdir(bands_path + dir):
                bands_path += dir + "/GRANULE/"

        bands_path += os.listdir(bands_path)[0] + "/IMG_DATA/R10m/"

        for file in os.listdir(bands_path):
            if path.isdir(bands_path) and "TCI" in file:
                shutil.move(bands_path + file, self.download_directory + product.tile_id + "/" + product.relative_orbit + "/" + product.date + "/" + file)
        
        bands_path = self.download_directory + product.tile_id + "/" + product.relative_orbit + "/" + product.date + "/"

        for file in os.listdir(bands_path):
            if path.isdir(bands_path + file):
                shutil.rmtree(bands_path + file)
        
        return bands_path

    def download_product_full(self, product, api):
        local_filename = self.download_directory + product.id + ".zip"
        
        try:
            with api.download_request(product) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
                        
        except requests.HTTPError as err:
                if err.response.status_code == 401:
                    api.regenerate_token_request()
                    if os.path.isfile(local_filename):
                        os.remove(local_filename)
                    with api.download_request(product) as r:
                        r.raise_for_status()
                        with open(local_filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192): 
                                f.write(chunk)
                else:
                    raise Exception("Не удалось выполнить загрузку продуктов.")

        except Exception:
            raise Exception("Не удалось выполнить загрузку продуктов.")
        
        with ZipFile(local_filename, 'r') as zObject:
                    zObject.extractall(path=self.download_directory)
        
        os.remove(local_filename)

    def download_product_train(self, product, api):
        local_filename = self.download_directory + product.id + ".zip"
        try:
            with api.download_request(product) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)  
        except requests.HTTPError as err:
                if err.response.status_code == 401:
                    api.regenerate_token_request()
                    if os.path.isfile(local_filename):
                        os.remove(local_filename)
                    with api.download_request(product) as r:
                        r.raise_for_status()
                        with open(local_filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192): 
                                f.write(chunk)
                else:
                    raise Exception("Не удалось выполнить загрузку продуктов.")

        except Exception:
            raise Exception("Не удалось выполнить загрузку продуктов.")
        
        with ZipFile(local_filename, 'r') as zObject:
                    zObject.extractall(path=self.download_directory)
        
        os.remove(local_filename)

        bands_path = self.download_directory
        for dir in os.listdir(bands_path):
            if os.path.isdir(bands_path + dir):
                bands_path += dir + "/GRANULE/"

        bands_path += os.listdir(bands_path)[0] + "/IMG_DATA/R10m/"

        for file in os.listdir(bands_path):
            if path.isdir(bands_path) and "TCI" in file:
                shutil.move(bands_path + file, self.download_directory + 'TCI.jp2')
            elif path.isdir(bands_path) and "B04" in file:
                shutil.move(bands_path + file, self.download_directory + 'B04.jp2')
            elif path.isdir(bands_path) and "B08" in file:
                shutil.move(bands_path + file, self.download_directory + 'B08.jp2')
        
        bands_path = self.download_directory

        for file in os.listdir(bands_path):
            if path.isdir(bands_path + file):
                shutil.rmtree(bands_path + file)    