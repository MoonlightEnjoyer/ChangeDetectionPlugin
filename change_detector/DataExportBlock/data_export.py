from .json_writer import JsonWriter
from .avro_writer import AvroWriter
from .csv_writer import CsvWriter
from .sql_writer import SqlWriter

class DataExport():

    def export_avro(self, coordinates, mask_path1, mask_path2, destination, progress_bar):
        avroWriter = AvroWriter()
        avroWriter.write_file(coordinates, mask_path1, mask_path2, destination, progress_bar)

    def export_csv(self, coordinates, mask_path1, mask_path2, destination, progress_bar):
        orcWriter = CsvWriter()
        orcWriter.write_file(coordinates, mask_path1, mask_path2, destination, progress_bar)

    def export_json(self, coordinates,  mask_path1, mask_path2, destination, progress_bar):
        jsonWriter = JsonWriter()
        jsonWriter.write_file(coordinates, mask_path1, mask_path2, destination, progress_bar)

    def export_sql(self, coordinates, mask_path1, mask_path2, connection_string, progress_bar):
        sqlWriter = SqlWriter()
        sqlWriter.write_file(coordinates, mask_path1, mask_path2, connection_string, progress_bar)