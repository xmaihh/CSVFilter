#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
RESOURCES_DIR="$SCRIPT_DIR/resources"

# Print current directory
echo "Current directory: $(pwd)"

# Run version.py script
python "$SCRIPT_DIR/prebuild_scripts/version.py"

# Run PyInstaller command
pyinstaller -F --add-data "$RESOURCES_DIR/*:resources/" --add-data "$SCRIPT_DIR/config.ini:." --icon="$RESOURCES_DIR/csv_filter.ico" -w --name CSVFilter "$SCRIPT_DIR/main.py"