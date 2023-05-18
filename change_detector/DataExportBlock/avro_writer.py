import cv2
import numpy as np
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from .data_writer import DataWriter

class AvroWriter(DataWriter):

    def write_file(self, coordinates, mask_path1, mask_path2, destination, progress_bar):
        mask1 = cv2.imread(mask_path1, cv2.IMREAD_UNCHANGED)
        mask2 = cv2.imread(mask_path2, cv2.IMREAD_UNCHANGED)

        data = {}

        counter = 0
        length = len(coordinates)

        with open("C:\\Users\\Artem\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\test_plugin\\DataExportBlock\\schema.avsc", "rb") as schema_file:
             schema = avro.schema.parse(schema_file.read())

        writer = DataFileWriter(open(destination, "wb"), DatumWriter(), schema)

        for c in coordinates:
                if mask1[c[0]][c[1]] != mask2[c[0]][c[1]]:
                    data[str(c[0]) + ',' + str(c[1])] = str(mask1[c[0]][c[1]]) + ',' + str(mask2[c[0]][c[1]])
                    writer.append({"x" : c[0], "y" : c[1], "old_class" : self.class_value_to_name(mask1[c[0]][c[1]]), "new_class" : self.class_value_to_name(mask2[c[0]][c[1]])})
                counter += 1
                progress_bar.setValue(int((counter / length) * 100))
        writer.close()        