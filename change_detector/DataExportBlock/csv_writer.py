import cv2
from .data_writer import DataWriter

class CsvWriter(DataWriter):

    def write_file(self, coordinates, mask_path1, mask_path2, destination, progress_bar):
        mask1 = cv2.imread(mask_path1, cv2.IMREAD_UNCHANGED)
        mask2 = cv2.imread(mask_path2, cv2.IMREAD_UNCHANGED)
        counter = 0
        length = len(coordinates)

        with open(destination, "w") as dest_file:
            for c in coordinates:
                if mask1[c[0]][c[1]] != mask2[c[0]][c[1]]:
                    dest_file.write(f'{c[0]},{c[1]},{self.class_value_to_name(mask1[c[0]][c[1]])},{self.class_value_to_name(mask2[c[0]][c[1]])}\n')
                counter += 1
                progress_bar.setValue(int((counter / length) * 100))