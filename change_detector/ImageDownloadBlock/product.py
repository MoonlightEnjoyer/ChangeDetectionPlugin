import re
from multipledispatch import dispatch

class Product():

    @dispatch(dict)
    def __init__(self, raw_product):
        self.id = raw_product['id']
        self.date = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', raw_product['properties']['startDate'])[0][:4]
        self.tile_id = re.findall('T[0-9]{2}[A-Z]{3}', raw_product['properties']['title'])[0]
        self.relative_orbit = re.findall('R[0-9]{3}', raw_product['properties']['title'])[0]
        self.clouds = float(str(raw_product['properties']['cloudCover']))

    @dispatch(str, str, str, str, float)
    def __init__(self, id, date, tile_id, relative_orbit, clouds):
        self.id = id
        self.date = date
        self.tile_id = tile_id
        self.relative_orbit = relative_orbit
        self.clouds = clouds

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.id == other.id and self.date == other.date and self.tile_id == other.tile_id and self.relative_orbit == other.relative_orbit and self.clouds == other.clouds
        return False