from csv_toolbox.lib_csv_filter.csv_filter import CSVFilter
from csv_toolbox.lib_csv_to_excel.csv_to_excel import CSVToExcel
from csv_toolbox.lib_excel_merge.excel_merger import ExcelMerger
from csv_toolbox.lib_excel_beautifier.excel_beautifier import ExcelBeautifier
from csv_toolbox.lib_data_preprocess.data_preprocess import DataPreprocess
from csv_toolbox.lib_utils.file import delete_file, rename_file
from csv_toolbox.lib_base.constants import (
    SHEET_NAME_ROW_DATA,
    SHEET_NAME_IOT_DATA,
    SHEET_NAME_BOX_DATA,
    XLSX_EXTENSION,
)


def helper_function(
    input_csv_file,
    filter_imeis=None,
    filter_imei_include=False,
    filter_macs=None,
    filter_mac_include=False,
):
    # 数据前处理 <DataPreprocess>
    preprocess = DataPreprocess(input_csv_file)
    preprocess.filter_imeis = filter_imeis
    preprocess.filter_imei_include = filter_imei_include
    preprocess.filter_macs = filter_macs
    preprocess.filter_mac_include = filter_mac_include
    preprocess.hidden_columns = ["预留Var7", "预留Var6", "预留Var5"]
    preprocess.preprocess()
    print(f"Step 1:::DataPreprocess output====={preprocess.save_to()}")

    # 筛选iot板信息 <CSVFilter>
    filter_iot = CSVFilter(preprocess.save_to())
    filter_iot.filter(lambda df: filter_iot.condition_filter_by_imei_prefix(df))
    print(f"Step 2:::CSVFilter <iot> output====={filter_iot.save_to()}")
    # 筛选盒子信息 <CSVFilter>
    filter_box = CSVFilter(preprocess.save_to())
    filter_box.filter(lambda df: ~filter_box.condition_filter_by_imei_prefix(df))
    print(f"Step 3:::CSVFilter <box> output====={filter_box.save_to()}")

    # 转换成Excel <CSVToExcel>
    row_coverter = CSVToExcel(preprocess.save_to())
    row_coverter.convert()
    print(f"Step 4:::CSVToExcel <row_data> output====={row_coverter.save_to()}")

    iot_coverter = CSVToExcel(filter_iot.save_to())
    iot_coverter.convert()
    print(f"Step 5:::CSVToExcel <iot> output====={iot_coverter.save_to()}")

    box_coverter = CSVToExcel(filter_box.save_to())
    box_coverter.convert()
    print(f"Step 6:::CSVToExcel <box> output====={box_coverter.save_to()}")

    # 合并多个Excel <ExcelMerger>
    merger = ExcelMerger(input_csv_file)
    merger.add_file(row_coverter.save_to(), SHEET_NAME_ROW_DATA)
    merger.add_file(iot_coverter.save_to(), SHEET_NAME_IOT_DATA)
    merger.add_file(box_coverter.save_to(), SHEET_NAME_BOX_DATA)
    merger.merge()
    print(f"Step 7:::ExcelMerger output====={merger.save_to()}")

    # 美化 <ExcelBeautifier>
    beautify = ExcelBeautifier(merger.save_to())
    beautify.beautify()
    print(f"Step 8:::ExcelBeautifier output====={beautify.save_to()}")

    # 重命名 <rename_file>
    output_excel = rename_file(beautify.save_to(), input_csv_file, XLSX_EXTENSION)
    print(f"Step 9:::output====={output_excel}")
    # 删除临时文件 <delete_file>
    delete_file(preprocess.save_to())
    delete_file(filter_iot.save_to())
    delete_file(filter_box.save_to())
    delete_file(row_coverter.save_to())
    delete_file(iot_coverter.save_to())
    delete_file(box_coverter.save_to())
    delete_file(merger.save_to())

    return output_excel
