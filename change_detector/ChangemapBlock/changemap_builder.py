import cv2
import numpy as np
import os

class ChangemapBuilder():

    def build_changemap(self, image_path, mask_path1, mask_path2, destination1, destination2, info_label):
        mask1 = cv2.imread(mask_path1, cv2.IMREAD_UNCHANGED)
        mask2 = cv2.imread(mask_path2, cv2.IMREAD_UNCHANGED)
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        try:
            mask1 = np.multiply(mask1, 0, out=mask1, where=mask1==5)
            mask2 = np.multiply(mask2, 0, out=mask2, where=mask2==5)
            changemap = np.subtract(mask1, mask2)
            changemap = changemap.astype(np.float64)
            changemap = np.power(changemap, 0, out=changemap, where=changemap!=0)
            kernel = np.ones((3, 3), dtype=np.uint8)
            changemap = cv2.erode(changemap, kernel, iterations=2)
            changemap = np.add(changemap, 254, out=changemap, where=changemap!=0)
            (b, g, r) = cv2.split(image)
            b = b.astype(np.float64)
            g = g.astype(np.float64)
            r = r.astype(np.float64)
            b = np.divide(b, changemap, out=b, where=changemap!=0)
            g = np.divide(g, changemap, out=g, where=changemap!=0)
            r = np.add(r, changemap)
            image = cv2.merge((b,g,r))
            cv2.imwrite(destination1 + "changemap.png", image)
            cv2.imwrite(destination1 + "contours.png", changemap)
            cv2.imwrite(destination2 + "changemap.png", image)
            cv2.imwrite(destination2 + "contours.png", changemap)
        except Exception as e:
            log = open(fr"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\log.txt", 'a')
            log.write("\n-> inside build_changemap()")
            log.write('\nException occured\n')
            log.write(str(e))
            log.write('\n#######################################\n')
            log.close()
            info_label.setText("Произошла ошибка при построении карты изменений")