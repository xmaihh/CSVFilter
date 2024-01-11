import pandas as pd
import os
import chardet
from csvfilter.const import const


class DataPreprocessor:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = self._convert_csv_to_dataframe()
        self.output_path = self._get_output_filepath()
        self.hidden_columns=None

    def _get_output_filepath(self):
        # 获取 CSV 文件所在的目录路径
        input_dir = os.path.dirname(self.input_path)
        # 获取 CSV 文件的文件名（不包含扩展名）
        input_filename = os.path.splitext(os.path.basename(self.input_path))[0]
        # 构建 Excel 文件的文件名
        output_filename = (
            f"{const.CSV_PREPROCESS_PREFIX}{input_filename}{const.CSV_FILE_SUFFIX}"
        )
        # 拼接 Excel 文件的完整路径
        output_path = os.path.join(input_dir, output_filename)
        print(output_path)
        return output_path

    def _get_file_encoding(self):
        # 检测文件编码
        # 获取检测到的编码格式
        with open(self.input_path, "rb") as f:
            result = chardet.detect(f.read())
            return result["encoding"]

    def _convert_csv_to_dataframe(self):
        # 读取 CSV 文件并将数据转换为 DataFrame
        # 返回 DataFrame
        try:
            df = pd.read_csv(self.input_path, encoding=self._get_file_encoding())
            return df
        except FileNotFoundError:
            raise Exception("CSV file not found.")
        except pd.errors.EmptyDataError:
            raise Exception("CSV file is empty.")
        except pd.errors.ParserError:
            raise Exception("Error parsing CSV file.")

    def preprocess(self, hidden_columns=None):
        version_dict = {}
        for index, row in self.df.iterrows():
            version_number = row["当前版本CurrentVersion"]
            version_description = row["版本说明VersionNote"]
            if version_number == "V1.40":
                version_dict[version_number] = f"当前为:ST最新版本{version_number}"
            elif version_number == "V2.11":
                version_dict[version_number] = f"当前为:FM最新版本{version_number}"
            elif version_number == "V1.39":
                version_dict[version_number] = f"当前为:ST设备不上线版本{version_number}"
            elif version_number == "V2.10":
                version_dict[version_number] = f"当前为:FM设备不上线版本{version_number}"
            elif version_number == "V1.38":
                version_dict[version_number] = f"当前为:ST流量异常版本{version_number}"
            elif version_number == "V2.09":
                version_dict[version_number] = f"当前为:FW流量异常版本{version_number}"
            elif version_number == "-":
                version_dict[version_number] = "-"
            else:
                version_dict[version_number] = f"当前为:其他版本{version_number}"

        self.df["版本说明VersionNote"] = self.df["当前版本CurrentVersion"].map(version_dict)

        if hidden_columns:
            self.df = self.df.drop(columns=hidden_columns)

        return self.df
    
    def set_hidden_columns(self,hidden_columns):
        self.hidden_columns = hidden_columns

    def save_to_csv(self):
        if self.hidden_columns:
            self.preprocess(self.hidden_columns).to_csv(self.output_path, index=False, encoding="utf_8_sig")
        else:
            self.preprocess().to_csv(self.output_path, index=False,encoding="utf_8_sig")

        print("新CSV文件已生成！")