# Import the helpers from the current folder "."
from . import helpers


def main_module_function():
    """
    +------------------------------------------------+
    |                                                |
    |             导入csv文件(data.csv)               |
    |                                                |
    +------------------------------------------------+
        |                                |
        |                                |
        |                                |
        V                                V
    +------------------------------------------------+
    |                                                |
    |     筛选数据                                    |
    |     条件：'唯一标识imei'是否'86'开头 == True     |
    |                                                |
    +------------------------------------------------+
        |                                |
        |                                |
        |                                |
        V                                V
    +------------------------------------------------+
    |                                                |
    |             导出到excel文件(output.xlsx)        |
    |             sheet1:原始数据                     |
    |             sheet2:符合条件的数据               |
    |             sheet3:不符合条件的数据             |
    |                                                |
    +------------------------------------------------+

    """
    solved = False
    input_file_csv = "D:/Downloads/93ff7950b5304878826fbed7190dd554.csv"  # 输入文件路径
    helpers.helper_function(input_file_csv)
    return solved
