from csvfilter.toexcel import create_csv_to_excel_converter
from csvfilter.tofilter import create_easily_filter_csv_file
from .helpers import const


def main_module_function():
    solved = False
    input_file = "D:/Downloads/93ff7950b5304878826fbed7190dd554.csv"  # 输入文件路径
    # 筛选iot板信息
    filter_iot_board = create_easily_filter_csv_file(input_file,const.EXCEL_FILE_PREFIX_IOT_CORE)
    iot_board_output_csv = filter_iot_board.filter_by_condition(filter_iot_board.filter_by_imei_prefix)
    # 筛选盒子信息
    filter_box = create_easily_filter_csv_file(input_file, const.EXCEL_FILE_PREFIX_UPGRADE_BOX)
    box_output_csv = filter_box.filter_by_condition(lambda df: ~filter_box.filter_by_imei_prefix(df))

    # toExcel
    iot_coverter = create_csv_to_excel_converter(iot_board_output_csv)
    iot_coverter.convert_csv_to_excel()

    box_coverter = create_csv_to_excel_converter(box_output_csv)
    box_coverter.convert_csv_to_excel()
    return solved
