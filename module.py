from csvfilter.tofilter import create_easily_filter_csv_file
from csvfilter.toexcel import create_csv_to_excel_converter
from csvfilter.tomerge import create_excel_merger
from csvfilter.tobeautify import create_beautify_excel
from .helpers import const
import os


def delete_file(file_path):
    """
    删除指定文件。

    Args:
        file_path (str): 要删除的文件的路径。
    """

    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
    else:
        raise ValueError(f"File '{file_path}' does not exist.")


def main_module_function():
    solved = False
    input_file_csv = "D:/Downloads/93ff7950b5304878826fbed7190dd554.csv"  # 输入文件路径
    # 筛选iot板信息
    filter_iot_board = create_easily_filter_csv_file(
        input_file_csv, const.EXCEL_FILE_PREFIX_IOT_CORE
    )
    iot_board_output_csv = filter_iot_board.filter_by_condition(
        filter_iot_board.filter_by_imei_prefix
    )
    # 筛选盒子信息
    filter_box = create_easily_filter_csv_file(
        input_file_csv, const.EXCEL_FILE_PREFIX_UPGRADE_BOX
    )
    box_output_csv = filter_box.filter_by_condition(
        lambda df: ~filter_box.filter_by_imei_prefix(df)
    )

    # toExcel
    row_data_coverter = create_csv_to_excel_converter(input_file_csv)
    excel_row_data = row_data_coverter.convert_csv_to_excel()

    iot_coverter = create_csv_to_excel_converter(iot_board_output_csv)
    excel_iot_data = iot_coverter.convert_csv_to_excel()

    box_coverter = create_csv_to_excel_converter(box_output_csv)
    excel_box_data = box_coverter.convert_csv_to_excel()

    # merge
    merger = create_excel_merger(input_file_csv)
    merger.add_file(excel_row_data, const.MERGE_FILE_SHEET_NAME_ROW_DATA)
    merger.add_file(excel_iot_data, const.MERGE_FILE_SHEET_NAME_IOT_DATA)
    merger.add_file(excel_box_data, const.MERGE_FILE_SHEET_NAME_BOX_DATA)
    mergedExcel = merger.merge_files()

    # 美化
    beautify = create_beautify_excel(mergedExcel)
    beautify.read_all_worksheets()

    # 删除临时文件
    delete_file(iot_board_output_csv)
    delete_file(box_output_csv)
    delete_file(excel_row_data)
    delete_file(excel_iot_data)
    delete_file(excel_box_data)

    return solved
