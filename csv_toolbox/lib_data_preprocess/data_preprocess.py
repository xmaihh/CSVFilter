import pandas as pd

from csv_toolbox.lib_base.base_filter import BaseFilter
from csv_toolbox.lib_base.constants import CSV_EXTENSION, DATA_PREPROCESS_PREFIX


class DataPreprocess(BaseFilter):
    def __init__(self, input_path):
        super().__init__(input_path, DATA_PREPROCESS_PREFIX, CSV_EXTENSION)
        self.hidden_columns = None
        self.filter_imeis = None
        self.filter_imei_include = False
        self.filter_macs = None
        self.filter_mac_include = False

    def _preprocess_data(self, hidden_columns=None):
        try:
            df = pd.read_csv(self.input_path, encoding=self._get_file_encoding())
        except FileNotFoundError:
            raise Exception("CSV file not found.")
        except pd.errors.EmptyDataError:
            raise Exception("CSV file is empty.")
        except pd.errors.ParserError:
            raise Exception("Error parsing CSV file.")
        # 筛选指定的数据
        if (
            self.filter_imeis is not None
            and isinstance(self.filter_imeis, list)
            and len(self.filter_imeis) != 0
        ):
            if self.filter_imei_include:
                for specified_imei in self.filter_imeis:
                    df = df[df["唯一标识imei"] == specified_imei]
            else:
                for specified_imei in self.filter_imeis:
                    df = df[df["唯一标识imei"] != specified_imei]
        if (
            self.filter_macs is not None
            and isinstance(self.filter_macs, list)
            and len(self.filter_macs) != 0
        ):
            if self.filter_mac_include:
                for specified_mac in self.filter_macs:
                    df = df[df["唯一标识imei"].str.contains(specified_mac)]
            else:
                for specified_mac in self.filter_macs:
                    df = df[~df["唯一标识imei"].str.contains(specified_mac)]
        # 剔除
        version_dict = {}
        for index, row in df.iterrows():
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

        df["版本说明VersionNote"] = df["当前版本CurrentVersion"].map(version_dict)

        if hidden_columns:
            missing_columns = [col for col in hidden_columns if col not in df.columns]

            if missing_columns:
                print(f"DataFrame do not exist: {missing_columns}")
            else:
                df = df.drop(columns=hidden_columns)
        # 返回新的CSV文件
        if self.hidden_columns:
            df.to_csv(self.output_path, index=False, encoding="utf_8_sig")
        else:
            df.to_csv(self.output_path, index=False, encoding="utf_8_sig")

    def preprocess(self):
        self._preprocess_data()
        self.save_to()
