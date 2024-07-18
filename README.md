# Quickstart

[![publish-to-release](https://github.com/xmaihh/CSVFilter/actions/workflows/publish-to-release.yml/badge.svg?branch=main)](https://github.com/xmaihh/CSVFilter/actions/workflows/publish-to-release.yml)

> ⚠️ CSVFilter works with **Python 3.7+**. To check your Python version, run [`python --version`](https://docs.python.org/3/using/cmdline.html#cmdoption-version).
>
> If you have both Python 2 and Python 3 installed, you may need to use `python3` instead of `python`. This is becoming less common as [Python 2 is sunsetting](https://www.python.org/doc/sunset-python-2/).

# TL;DR

1. [Creating virtual environments](./docs/1. Creating virtual environments.md)
2. [Create a `requirements.txt` File](./docs/2. Create a requirements.txt File.md)

# Requirements

The [**requirements.txt**](./requirements.txt) is a simple text file which lists the dependencies, or necessary packages that are required to run the code.
Install the required packages from `requirements.txt`

```shell
pip install -r requirements.txt
```


# Usage

The program can then be executed from a command line using the `main.py` executable:

```shell
→ D:\<your-local-directory>\CSVFilter [main]› python main.py
```

# Executables

Make sure you have the `Requirements` installed, and then install PyInstaller from PyPI:

```
pip install -U pyinstaller
```

Open a command prompt/shell window, and navigate to the directory where `main.py` file is located, then build app with the following command:

```
pyinstaller main.py
```

Your bundled application should now be available in the dist folder.

```shell
pyinstaller -F --add-data "resources/*;resources/" --add-data "config.ini;."  --icon=.\resources\csv_filter.ico -w --clean --name CSVFilter main.py
```


# The project folder follows this structure:

```
├── CSVFilter/
    ├── csv_toolbox
    │   ├── data
    │   ├── lib_base
    │   ├── lib_csv_filter
    │   ├── lib_csv_to_excel
    │   ├── lib_data_preprocess
    │   ├── lib_excel_beautifier
    │   ├── lib_excel_merge
    │   ├── lib_i18n
    │   ├── lib_log
    │   └── lib_utils
    ├── docs
    ├── resources
    ├── scripts
    └── tests
```
