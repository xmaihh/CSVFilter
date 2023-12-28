import os
import openpyxl
import pandas as pd
import chardet

from csvfilter.toexcel import create_csv_to_excel_converter


def print_progress(current, total):
    """打印任务进度"""
    text = f"Progress: {current}/{total}"
    print(text, end="\r", flush=True)


def csv_to_xlsx_pd():
    filepath = "D:/Downloads/93ff7950b5304878826fbed7190dd554.csv"
    # 获取文件名（不包含扩展名）
    print_progress(1, "获取文件名")
    filename = os.path.splitext(os.path.basename(filepath))[0]
    # 修改文件路径，添加 ".xlsx" 后缀
    print_progress(2, "修改文件路径")
    new_filepath = os.path.join(os.path.dirname(filepath), filename + ".xlsx")
    with open(filepath, "rb") as f:
        result = chardet.detect(f.read())  # 检测文件编码
    encoding = result["encoding"]  # 获取检测到的编码格式
    print_progress(3, f"检测csv文件编码:{encoding}")
    csv = pd.read_csv(filepath, encoding=encoding)
    csv.to_excel(new_filepath, sheet_name="row_data")

    # 美化
    # 打开生成的Excel文件
    print_progress(4, "美化xlsx文件")
    workbook = openpyxl.load_workbook(new_filepath)
    worksheet = workbook.active
    print_progress(5, "设置动态列宽")
    # 遍历每一列的单元格内容，动态调整列宽度
    for column in worksheet.columns:
        max_length = 0
        # 获取列名
        for cell in column:
            try:  # 避免空单元格引发TypeError
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 4) * 1.2  # 乘以一个调整系数，可以根据实际情况调整
        column_letter = column[0].column_letter  # 获取列的字母标识
        worksheet.column_dimensions[column_letter].width = adjusted_width
        print_progress(6, f"正在设置...{column_letter}的列宽为{adjusted_width}")

    # 保存修改后的Excel文件
    workbook.save(new_filepath)
    print_progress(7, f"已保存至{new_filepath}")


def filter_and_display():
    filepath = "D:/Downloads/93ff7950b5304878826fbed7190dd554.csv"

    with open(filepath, "rb") as f:
        result = chardet.detect(f.read())  # 检测文件编码
    encoding = result["encoding"]  # 获取检测到的编码格式

    data = pd.read_csv(filepath, encoding=encoding)

    # 定义筛选条件
    condition = data["唯一标识imei"].str.startswith("86")
    # 根据筛选条件筛选数据
    df_filtered = data[condition]
    df_not_filtered = data[~condition]
    # 将筛选结果保存到新的 CSV 文件
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    new_filepath = os.path.join(directory, "filtered_" + filename)
    not_filtered_filepath = os.path.join(directory, "not_filtered_" + filename)

    if df_filtered.empty:  # 如果筛选结果为空
        print("没有符合条件的数据！")
    else:
        df_filtered.to_csv(new_filepath, index=False, encoding="utf_8_sig")
        df_not_filtered.to_csv(not_filtered_filepath,index=False,encoding="utf_8_sig")
        # 在这里你可以选择如何展示筛选结果，比如使用 print()、展示在另一个窗口等方式
        # print(df_filtered)
        print(new_filepath)
        print(not_filtered_filepath)


if __name__ == "__main__":
    # csv_to_xlsx_pd()
    # filter_and_display()
    # 创建 CsvToExcelConverter 对象


    csv_filepath = "D:/Downloads/93ff7950b5304878826fbed7190dd554.csv"
    converter = create_csv_to_excel_converter(csv_filepath)