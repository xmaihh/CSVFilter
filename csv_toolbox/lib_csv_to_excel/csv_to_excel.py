import pandas as pd
from csv_toolbox.lib_base.base_filter import BaseFilter
from csv_toolbox.lib_base.constants import CSV_TO_EXCEL_PREFIX, XLSX_EXTENSION


class CSVToExcel(BaseFilter):
    def __init__(self, input_path):
        super().__init__(input_path, CSV_TO_EXCEL_PREFIX, XLSX_EXTENSION)

    def _convert_to_excel(self):
        try:
            df = pd.read_csv(self.input_path, encoding=self._get_file_encoding())
        except FileNotFoundError:
            raise Exception("CSV file not found.")
        except pd.errors.EmptyDataError:
            raise Exception("CSV file is empty.")
        except pd.errors.ParserError:
            raise Exception("Error parsing CSV file.")
        df.to_excel(self.output_path)

    def convert(self):
        self._convert_to_excel()
        self.save_to()
