import pandas as pd
from csv_toolbox.lib_base.base_filter import BaseFilter
from csv_toolbox.lib_base.constants import EXCEL_MERGE_PREFIX, XLSX_EXTENSION


class ExcelMerger(BaseFilter):
    def __init__(self, input_path):
        super().__init__(input_path, EXCEL_MERGE_PREFIX, XLSX_EXTENSION)
        self.excel_files = []
        self.sheet_names = []

    def add_file(self, file_path, sheet_name):
        """
        添加要合并的excel文件路径和对应的sheet名称

        :param file_path: 要添加的excel文件路径
        :param sheet_name: 合并后的sheet名称
        """
        self.excel_files.append(file_path)
        self.sheet_names.append(sheet_name)

    def _merge_excel_files(self):
        if not self.excel_files:
            raise ValueError("No excel files added.")
        writer = pd.ExcelWriter(self.output_path, engine="openpyxl")
        for i in range(len(self.excel_files)):
            file_path = self.excel_files[i]
            sheet_name = self.sheet_names[i]
            df = pd.read_excel(file_path)

            def deal_str(data):
                data = str(data) + "\t"
                return data

            # Now, when you export the df DataFrame to a csv file, all the data in the imei column will be stored as strings, without using scientific notation(with E).
            df["唯一标识imei"] = df["唯一标识imei"].map(deal_str)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer._save()

    def merge(self):
        self._merge_excel_files()
        self.save_to()
