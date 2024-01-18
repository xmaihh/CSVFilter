# Import the helpers from the current folder "."
from csv_toolbox import CSVFilterApp


def main_module_function():
    """
    +---------------------------------------------------+
    |                                                   |
    |             Import csv file (data.csv)            |
    |                                                   |
    +---------------------------------------------------+
        |                                |
        |                                |
        |                                |
        V                                V
    +-----------------------------------------------------------------------------+
    |                                                                             |
    |             Filter data                                                     |
    |             Condition: 'Unique identifier imei' starts with '86' == True    |
    |                                                                             |
    +-----------------------------------------------------------------------------+
        |                                |
        |                                |
        |                                |
        V                                V
    +----------------------------------------------------------------------------+
    |                                                                            |
    |             Export to excel file (output.xlsx)                             |
    |             sheet1: original data                                          |
    |             sheet2: data that meets the condition                          |
    |             sheet3: data that does not meet the condition                  |
    |                                                                            |
    +----------------------------------------------------------------------------+

    """
    app = CSVFilterApp()
    app.run()
