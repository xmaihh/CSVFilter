import os
import pandas as pd
import chardet


class CSVFilter:
    def __init__(self, input_file, output_file_prefix):
        self.input_file = input_file
        self.output_file_prefix = output_file_prefix
        self.output_file = self._get_output_file_path()

    def _get_output_file_path(self):
        input_dir = os.path.dirname(self.input_file)
        input_file_name = os.path.basename(self.input_file)
        output_file_name = self.output_file_prefix + input_file_name
        output_file_path = os.path.join(input_dir, output_file_name)
        print(output_file_path)
        return output_file_path

    def filter(self, condition):
        # 检测文件编码
        with open(self.input_file, "rb") as file:
            result = chardet.detect(file.read())
        encoding = result["encoding"]
        # 读取 CSV 文件为 DataFrame
        df = pd.read_csv(self.input_file, encoding=encoding)
        # 根据条件筛选 DataFrame 的行
        filtered_df = df[condition(df)]
        if filtered_df.empty:  # 如果筛选结果为空
            print("没有符合条件的数据！")
            return None
        else:
            filtered_df.to_csv(self.output_file, index=False, encoding="utf_8_sig")
            print(f"Save CSV file. Saved to {self.output_file}")
            return self.output_file

    def filter_by_imei_prefix(self, df):
        # 在这里编写 IMEI 号前缀筛选条件逻辑
        # 返回一个布尔 Series，表示每一行是否满足条件
        # 例如：只保留 'imei' 列中值以 "86" 开头的行
        return df["唯一标识imei"].str.startswith("86")
