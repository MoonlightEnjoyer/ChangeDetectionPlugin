import os
import cv2

class ImagePreprocessor():
    def remove_clouds(self, images_path):
        images = []
        for image in os.listdir(images_path):
            images.append(images_path + image)
        
        if len(images) < 2:
            base_image = cv2.imread(images[0], cv2.IMREAD_UNCHANGED)
            cv2.imwrite(images_path + "clouds_removed.jp2", base_image)
        else:
            base_image = cv2.imread(images[0], cv2.IMREAD_UNCHANGED)
            reserve_image = cv2.imread(images[1], cv2.IMREAD_UNCHANGED)

            for i in range(10980):
                for j in range(10980):
                    if (int(base_image[i][j][0]) + int(base_image[i][j][1]) + int(base_image[i][j][2])) / 3 > 120 and (int(reserve_image[i][j][0]) + int(reserve_image[i][j][1]) + int(reserve_image[i][j][2])) / 3 < 120:
                        base_image[i][j] = reserve_image[i][j]
            
            cv2.imwrite(images_path + "clouds_removed.jp2", base_image)