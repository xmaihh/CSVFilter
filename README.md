# Quickstart

> ⚠️ CSVFilter works with **Python 3.7+**. To check your Python version, run [`python --version`](https://docs.python.org/3/using/cmdline.html#cmdoption-version).
>
> If you have both Python 2 and Python 3 installed, you may need to use `python3` instead of `python`. This is becoming less common as [Python 2 is sunsetting](https://www.python.org/doc/sunset-python-2/).

## Requirements

The [**requirements.txt**](./requirements.txt) is a simple text file which lists the dependencies, or necessary packages that are required to run the code.
Install the required packages from `requirements.txt`

```shell
pip install -r requirements.txt
```


## Usage

The program can then be executed from a command line using the `main.py` executable:

```shell
→ D:\<your-local-directory>\CSVFilter [main]› python main.py
```

## Executables

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
    ├── tests/
    │   ├── windchill.py
    │   ├── basic_test.py
    │   └── __init__.py
    ├── resources/
    │   ├── windchill.png
    │   └── csv_filter.ico
    ├── requirements.txt
    ├── requirements.in
    ├── main.py
    ├── docs/
    ├── csvfilter.log
    ├── csvfilter/
    │   ├── version.py
    │   ├── tomerge/
    │   │   ├── excel_merger.py
    │   │   └── __init__.py
    │   ├── tofilter/
    │   │   ├── easily_filter_csv_file.py
    │   │   └── __init__.py
    │   ├── toexcel/
    │   │   ├── csv_to_excel_converter.py
    │   │   └── __init__.py
    │   ├── tobeautify/
    │   │   ├── beautify_excel.py
    │   │   └── __init__.py
    │   ├── preprocess/
    │   │   ├── csv_preprocess.py
    │   │   └── __init__.py
    │   ├── module.py
    │   ├── logger.py
    │   ├── helpers.py
    │   ├── csv_filter.py
    │   ├── const.py
    │   └── __init__.py
    └── README.md
```
