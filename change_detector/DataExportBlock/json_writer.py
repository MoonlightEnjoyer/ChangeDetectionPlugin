import json
import cv2
from .data_writer import DataWriter

class JsonWriter(DataWriter):

    def write_file(self, coordinates,  mask_path1, mask_path2, destination, progress_bar):
        mask1 = cv2.imread(mask_path1, cv2.IMREAD_UNCHANGED)
        mask2 = cv2.imread(mask_path2, cv2.IMREAD_UNCHANGED)
        data = {}
        counter = 0
        length = len(coordinates)

        with open(destination, 'a') as destination_json:
            for c in coordinates:
                    if mask1[c[0]][c[1]] != mask2[c[0]][c[1]]:
                        data[str(c[0]) + ',' + str(c[1])] = self.class_value_to_name(mask1[c[0]][c[1]]) + ',' + self.class_value_to_name(mask2[c[0]][c[1]])
                        json.dump(json.dumps(data), destination_json)
                    counter += 1
                    progress_bar.setValue(int((counter / length) * 100))