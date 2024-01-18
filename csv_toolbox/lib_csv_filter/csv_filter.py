import pandas as pd
from csv_toolbox.lib_base.base_filter import BaseFilter
from csv_toolbox.lib_base.constants import CSV_FILTER_PREFIX, CSV_EXTENSION


class CSVFilter(BaseFilter):
    def __init__(self, input_path):
        super().__init__(input_path, CSV_FILTER_PREFIX, CSV_EXTENSION)

    def _filter_csv(self, condition):
        try:
            df = pd.read_csv(self.input_path, encoding=self._get_file_encoding())
        except FileNotFoundError:
            raise Exception("CSV file not found.")
        except pd.errors.EmptyDataError:
            raise Exception("CSV file is empty.")
        except pd.errors.ParserError:
            raise Exception("Error parsing CSV file.")
        filtered_df = df[condition]
        if filtered_df.empty:
            print("no matching data!")
        else:
            filtered_df.to_csv(self.output_path, index=False, encoding="utf_8_sig")

    def condition_filter_by_imei_prefix(self, df):
        """Filters the DataFrame by IMEI prefix.

        This method takes a DataFrame `df` as input and returns a Boolean Series, where each
        value indicates whether the corresponding row satisfies the filtering condition.

        Args:
            df: The DataFrame to filter.

        Returns:
            A Boolean Series indicating which rows satisfy the filtering condition.

        Example:
            Only keep rows where the 'imei' column starts with "86":

            ```python
            import pandas as pd
            df = pd.DataFrame({"imei": ["861234567890", "911234567890", "862345678901"]})
            filtered_df = df[condition_filter_by_imei_prefix(df)]
            print(filtered_df)
            ```

            Output:

            ```
            imei
            0  861234567890
            2  862345678901
            ```
        """
        return df["唯一标识imei"].str.startswith("86")

    def filter(self, condition):
        self._filter_csv(condition)
        self.save_to()
