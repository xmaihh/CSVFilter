import os
import pandas as pd
import chardet

class EasillyFilterCSVFile:
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

    def filter_by_condition(self, condition):
        # 检测文件编码
        with open(self.input_file, 'rb') as file:
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
        return df['唯一标识imei'].str.startswith("86")

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
        df_not_filtered.to_csv(not_filtered_filepath, index=False, encoding="utf_8_sig")
        # 在这里你可以选择如何展示筛选结果，比如使用 print()、展示在另一个窗口等方式
        # print(df_filtered)
        print(new_filepath)
        print(not_filtered_filepath)


if __name__ == "__main__":
    # filter_and_display()
    input_file = "D:/Downloads/93ff7950b5304878826fbed7190dd554.csv"  # 输入文件路径
    # output_file_prefix = "CSVFilter_IotCore_"  # 输出文件名
    output_file_prefix = "CSVFilter_UpgradeBox_"

    csv_filter = EasillyFilterCSVFile(input_file, output_file_prefix)

    # 按照 IMEI 号前缀筛选
    # csv_filter.filter_by_condition(csv_filter.filter_by_imei_prefix)
    csv_filter.filter_by_condition(lambda df: ~csv_filter.filter_by_imei_prefix(df))

