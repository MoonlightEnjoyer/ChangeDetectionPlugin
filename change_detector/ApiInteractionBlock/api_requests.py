import requests
import json
from multipledispatch import dispatch

class ApiRequests():

    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.access_token = ''
        self.refresh_token = ''

    def token_request(self):
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

        payload = {
            'grant_type' : 'password',
            'username' : self.username,
            'password' : self.password,
            'client_id' : 'cdse-public'
        }

        response = requests.post(url, headers=headers, data=payload)
        self.access_token = json.loads(response.content)['access_token']
        self.refresh_token = json.loads(response.content)['refresh_token']

    def regenerate_token_request(self):
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

        payload = {
            'grant_type' : 'refresh_token',
            'refresh_token' : self.refresh_token,
            'client_id' : 'cdse-public'
        }

        response = requests.post(url, headers=headers, data=payload)
        self.access_token = json.loads(response.content)['access_token']
        self.refresh_token = json.loads(response.content)['refresh_token']

    @dispatch(float, float, int, max_cloud_cover = float)
    def images_data_request(self, lat, lon, year, max_cloud_cover = 100.0):
        url = 'https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?'
        params = {
            'cloudCover' : f'[0,{max_cloud_cover}]',
            'startDate' : str(year) + '-06-10',
            'completionDate' : str(year) + '-06-30',
            'productType' : 'S2MSI2A',
            'processingLevel' : '   ',
            'lon' : str(lon),
            'lat' : str(lat)
        }

        for param in params.items():
            url += param[0] + '=' + param[1] + '&'

        url = url[:-1]
        response = requests.get(url)

        products_info = json.loads(response.content)
        return products_info
    
    @dispatch(float, float, str, str, float, max_records = int)
    def images_data_request(self, lat, lon, date1, date2, max_cloud_cover, max_records = 20):
        url = 'https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?'
        params = {
            'cloudCover' : f'[0,{max_cloud_cover}]',
            'startDate' : date1,
            'completionDate' : date2,
            'productType' : 'S2MSI2A',
            'processingLevel' : 'S2MSI2A',
            'lon' : str(lon),
            'lat' : str(lat),
            'maxRecords' : str(max_records)
        }

        for param in params.items():
            url += param[0] + '=' + param[1] + '&'

        url = url[:-1]
        response = requests.get(url)

        products_info = json.loads(response.content)
        return products_info

    def download_request(self, product):
        url = 'https://catalogue.dataspace.copernicus.eu/odata/v1/Products(' + product.id + ')/$value'

        headers = {
            'Authorization' : "Bearer " + self.access_token,
            'Content-Type' : 'application/json'
        }

        return requests.get(url, headers=headers, stream=True)