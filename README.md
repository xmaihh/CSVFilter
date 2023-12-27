
# 操作命令

```
.\venv\Scripts\activate.ps1
pip install  pyinstaller
pip install pillow
pyinstaller -F --add-data "resources/*.png;resources/" --icon=.\resources\csv_filter.ico -w --debug all CSVFilter.py
```

# 打包成.exe

```
 pyinstaller -F --add-data "resources/*.png;resources/" --icon=.\resources\csv_filter.ico -w --debug all CSVFilter.py
```