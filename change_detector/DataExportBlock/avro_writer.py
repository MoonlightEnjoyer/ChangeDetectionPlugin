import cv2
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
import os

from .data_writer import DataWriter

class AvroWriter(DataWriter):

    def write_file(self, coordinates, mask_path1, mask_path2, destination, progress_bar):
        mask1 = cv2.imread(mask_path1, cv2.IMREAD_UNCHANGED)
        mask2 = cv2.imread(mask_path2, cv2.IMREAD_UNCHANGED)
        plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data = {}
        counter = 0
        length = len(coordinates)

        with open(fr"{plugin_dir}\DataExportBlock\schema.avsc", "rb") as schema_file:
             schema = avro.schema.parse(schema_file.read())

        writer = DataFileWriter(open(destination, "wb"), DatumWriter(), schema)

        for c in coordinates:
                if mask1[c[0]][c[1]] != mask2[c[0]][c[1]]:
                    data[str(c[0]) + ',' + str(c[1])] = str(mask1[c[0]][c[1]]) + ',' + str(mask2[c[0]][c[1]])
                    writer.append({"x" : c[0], "y" : c[1], "old_class" : self.class_value_to_name(mask1[c[0]][c[1]]), "new_class" : self.class_value_to_name(mask2[c[0]][c[1]])})
                counter += 1
                progress_bar.setValue(int((counter / length) * 100))
        writer.close()        