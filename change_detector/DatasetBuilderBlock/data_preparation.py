import cv2
import numpy as np
import gc

class DataPreparation:
    def mark_masks_color(self, source, destination):
        image_red = cv2.imread(source + 'B04.jp2', cv2.IMREAD_UNCHANGED)
        image_nir = cv2.imread(source + 'B08.jp2', cv2.IMREAD_UNCHANGED)
        image_tci = cv2.imread(source + 'TCI.jp2', cv2.IMREAD_UNCHANGED)
        
        image_nir = image_nir.astype(np.int32)
        image_red = image_red.astype(np.int32)

        subtracted = np.subtract(image_nir, image_red)
        added = np.add(image_nir, image_red)
        ndvi = np.divide(subtracted, added, where=added!=0)
        ndvi = np.add(ndvi, 1, where=ndvi!=0)
        ndvi = np.multiply(ndvi, 255/2)

        ignore_mask = np.add(image_nir, 1, where=image_nir==0)
        cv2.imwrite(destination + 'ignore.png', ignore_mask)

        del image_nir
        del image_red
        del ignore_mask
        gc.collect()

        water_mask = np.add(ndvi, 0, where=(ndvi<130))

        buildings_mask = np.add(ndvi, 0, where=(np.logical_and(130 < ndvi, ndvi < 140)))
        farmland_mask = np.add(ndvi, 0, where=(np.logical_and(140 < ndvi, ndvi < 170)))

        (blue, green, red) = cv2.split(image_tci)
        grass_mask = np.add(ndvi, green, where=(np.logical_and(np.logical_and(170 < ndvi, ndvi < 255), green > 55)))
        forest_mask = np.add(ndvi, green, where=(np.logical_and(np.logical_and(170 < ndvi, ndvi < 255), green < 55)))

        del ndvi
        gc.collect()

        water_mask = np.power(water_mask, 0, where=water_mask!=0)
        buildings_mask = np.power(buildings_mask, 0, where=buildings_mask!=0)
        farmland_mask = np.power(farmland_mask, 0, where=farmland_mask!=0)
        grass_mask = np.power(grass_mask, 0, where=grass_mask!=0)
        forest_mask = np.power(forest_mask, 0, where=forest_mask!=0)
        
        red = red * 0.2126
        green = green * 0.7152
        blue = blue * 0.0722

        brightness_map = red + green
        brightness_map = brightness_map + blue

        del red
        del green
        del blue
        gc.collect()

        brightness_map = brightness_map - 229
        
        clouds_mask = np.add(0, brightness_map, where=brightness_map>0)
        clouds_mask = np.multiply(clouds_mask, 200)
        clouds_mask = np.power(clouds_mask, 0, where=clouds_mask!=0)

        cv2.imwrite(destination + 'water.png', water_mask)
        cv2.imwrite(destination + 'buildings.png', buildings_mask)
        cv2.imwrite(destination + 'farmland.png', farmland_mask)
        cv2.imwrite(destination + 'grass.png', grass_mask)
        cv2.imwrite(destination + 'forest.png', forest_mask)
        cv2.imwrite(destination + 'clouds.png', clouds_mask)