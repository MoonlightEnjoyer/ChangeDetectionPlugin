import cv2
import numpy as np

class ResultsAnalyser():
    
    def get_changed_areas_coords(self, directory):
        image = cv2.imread(directory + 'contours.png', cv2.IMREAD_UNCHANGED)
        blur = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
        ret, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)
        cv2.imwrite(directory +"thresh.png", thresh)
        contours, hierarchies = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        blank = np.zeros(thresh.shape[:2], dtype='uint8')
        cv2.drawContours(blank, contours, -1, (255, 0, 0), 1)
        cv2.imwrite(directory + "contours_blank.png", blank)
        colored_image = np.zeros((10980, 10980, 3), dtype=np.uint8)
        changed_areas_coordinates = []
        for i in contours:
            M = cv2.moments(i)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.drawContours(colored_image, [i], -1, (0, 255, 0), 2)
                cv2.circle(colored_image, (cx, cy), 7, (0, 0, 255), -1)
                cv2.putText(colored_image, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                changed_areas_coordinates.append((cx, cy))
        cv2.imwrite(directory + "marked_middle.png", colored_image)
        return changed_areas_coordinates