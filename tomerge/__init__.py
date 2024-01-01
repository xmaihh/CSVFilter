from .excel_merger import ExcelMerger


def create_excel_merger(csv_filepath):
    return ExcelMerger(csv_filepath)


__all__ = ["create_excel_merger"]
