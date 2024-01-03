from .beautify_excel import BeautifyExcel


def create_beautify_excel(excel_filepath):
    return BeautifyExcel(excel_filepath)


__all__ = ["create_beautify_excel"]
