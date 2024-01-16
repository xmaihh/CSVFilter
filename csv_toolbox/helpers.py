from csv_toolbox.lib_csv_filter.csv_filter import CSVFilter
from csv_toolbox.lib_csv_to_excel.csv_to_excel import CSVToExcel
from csv_toolbox.lib_excel_merge.excel_merger import ExcelMerger
from csv_toolbox.lib_excel_beautifier.excel_beautifier import ExcelBeautifier
from csv_toolbox.lib_data_preprocess.data_preprocess import DataPreprocess
from .lib_base.constants import (
    EXCEL_FILE_PREFIX_IOT_CORE,
    EXCEL_FILE_PREFIX_UPGRADE_BOX,
    MERGE_FILE_SHEET_NAME_ROW_DATA,
    MERGE_FILE_SHEET_NAME_IOT_DATA,
    MERGE_FILE_SHEET_NAME_BOX_DATA,
)
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


def helper_function(
    input_csv_file,
    filter_imeis=None,
    filter_imei_include=False,
    filter_macs=None,
    filter_mac_include=False,
):
    # 数据前处理
    preprocess = DataPreprocess(input_csv_file)
    preprocess.filter_imeis = filter_imeis
    preprocess.filter_imei_include = filter_imei_include
    preprocess.filter_macs = filter_macs
    preprocess.filter_mac_include = filter_mac_include
    preprocess.hidden_columns = ["预留Var7", "预留Var6", "预留Var5"]
    preprocess.save_to_csv()

    # 筛选iot板信息
    filter_iot_board = CSVFilter(preprocess.output_path, EXCEL_FILE_PREFIX_IOT_CORE)
    iot_board_output_csv = filter_iot_board.filter(
        filter_iot_board.filter_by_imei_prefix
    )
    # 筛选盒子信息
    filter_box = CSVFilter(preprocess.output_path, EXCEL_FILE_PREFIX_UPGRADE_BOX)
    box_output_csv = filter_box.filter(lambda df: ~filter_box.filter_by_imei_prefix(df))

    # toExcel
    row_data_coverter = CSVToExcel(preprocess.output_path)
    excel_row_data = row_data_coverter.convert()

    iot_coverter = CSVToExcel(iot_board_output_csv)
    excel_iot_data = iot_coverter.convert()

    box_coverter = CSVToExcel(box_output_csv)
    excel_box_data = box_coverter.convert()

    # merge
    merger = ExcelMerger(input_csv_file)
    merger.add_file(excel_row_data, MERGE_FILE_SHEET_NAME_ROW_DATA)
    merger.add_file(excel_iot_data, MERGE_FILE_SHEET_NAME_IOT_DATA)
    merger.add_file(excel_box_data, MERGE_FILE_SHEET_NAME_BOX_DATA)
    mergedExcel = merger.merge()

    # 美化
    beautify = ExcelBeautifier(mergedExcel)
    beautify.read_all_worksheets()

    # 删除临时文件
    delete_file(preprocess.output_path)
    delete_file(iot_board_output_csv)
    delete_file(box_output_csv)
    delete_file(excel_row_data)
    delete_file(excel_iot_data)
    delete_file(excel_box_data)

    return mergedExcel
