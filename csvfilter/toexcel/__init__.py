from .csv_to_excel_converter import CsvToExcelConverter


def create_csv_to_excel_converter(csv_filepath):
    return CsvToExcelConverter(csv_filepath)


__all__ = ["create_csv_to_excel_converter"]
