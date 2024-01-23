@echo off
setlocal

set SCRIPT_DIR=%~dp0
set RESOURCES_DIR=%SCRIPT_DIR%resources

rem Print current directory
echo Current directory: %cd%

rem Run version.py script
python "%SCRIPT_DIR%prebuild_scripts\version.py"

rem Run PyInstaller command
pyinstaller -F --add-data "%RESOURCES_DIR%\*;resources/" --add-data "%SCRIPT_DIR%config.ini;." --icon="%RESOURCES_DIR%\csv_filter.ico" -w --name CSVFilter "%SCRIPT_DIR%main.py"