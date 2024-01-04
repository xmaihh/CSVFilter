import os
import pandas as pd
from ..const import const


class ExcelMerger:
    def __init__(self, csv_filepath):
        self.csv_filepath = csv_filepath
        self.excel_files = []
        self.sheet_names = []
        self.merged_file = self._get_excel_filepath()

    def _get_excel_filepath(self):
        # 获取 CSV 文件所在的目录路径
        csv_dir = os.path.dirname(self.csv_filepath)
        # 获取 CSV 文件的文件名（不包含扩展名）
        csv_filename = os.path.splitext(os.path.basename(self.csv_filepath))[0]
        # 构建 Excel 文件的文件名
        excel_filename = f"{csv_filename}{const.EXCEL_FILE_SUFFIX}"
        # 拼接 Excel 文件的完整路径
        excel_filepath = os.path.join(csv_dir, excel_filename)
        print(excel_filepath)
        return excel_filepath

    def add_file(self, file_path, sheet_name):
        """
        添加要合并的excel文件路径和对应的sheet名称

        :param file_path: 要添加的excel文件路径
        :param sheet_name: 合并后的sheet名称
        """
        self.excel_files.append(file_path)
        self.sheet_names.append(sheet_name)

    def merge_files(self):
        """
        将多个excel文件合并成一个，每个文件放在一个单独的sheet中

        :return: 新的excel文件路径
        """
        if not self.excel_files:
            raise ValueError("No excel files added.")

        # 创建新的excel文件
        writer = pd.ExcelWriter(self.merged_file, engine="openpyxl")

        # 遍历所有要合并的excel文件
        for i in range(len(self.excel_files)):
            file_path = self.excel_files[i]
            sheet_name = self.sheet_names[i]

            # 读取当前excel文件中的数据到DataFrame中
            df = pd.read_excel(file_path)

            def deal_str(data):
                data = str(data) + "\t"
                return data

            # Pandas 较长数字数据导出csv文件后变成科学计数法（带E）的解决办法
            df["唯一标识imei"] = df["唯一标识imei"].map(deal_str)
            # 将DataFrame写入新文件中的指定sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # 保存新的excel文件
        writer._save()
        # merge_multiple_excel_files_into_one
        # 返回新的excel文件路径
        return self.merged_file
