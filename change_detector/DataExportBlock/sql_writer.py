import cv2
import psycopg2
from psycopg2 import sql
from .data_writer import DataWriter

class SqlWriter(DataWriter):

    def write_file(self, coordinates, mask_path1, mask_path2, destination, progress_bar):
        mask1 = cv2.imread(mask_path1, cv2.IMREAD_UNCHANGED)
        mask2 = cv2.imread(mask_path2, cv2.IMREAD_UNCHANGED)
        counter = 0
        length = len(coordinates)
        connection = psycopg2.connect(destination)
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE TYPE IF NOT EXISTS coordinates AS (lat integer, lon integer);"))
        cursor.execute(sql.SQL("CREATE TABLE IF NOT EXISTS %s (coordinates coordinates PRIMARY KEY NOT NULL, old_class VARCHAR NOT NULL, new_class VARCHAR NOT NULL)" % "test_table"))
        connection.commit()

        for c in coordinates:
                if mask1[c[0]][c[1]] != mask2[c[0]][c[1]]:
                    cursor.execute(sql.SQL("INSERT INTO %s (coordinates, old_class, new_class) VALUES (ROW(%d, %d), '%s', '%s') ON CONFLICT (coordinates) DO NOTHING" % ("test_table", c[0], c[1], self.class_value_to_name(mask1[c[0]][c[1]]), self.class_value_to_name(mask2[c[0]][c[1]]))))
                    connection.commit()
                counter += 1
                progress_bar.setValue(int((counter / length) * 100))
        cursor.close()
        connection.close()