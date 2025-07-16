@echo off
chcp 65001 > nul
echo ==========================================
echo         PDF拆分工具 - 自动打包脚本
echo ==========================================
echo.

echo [1/5] 检查环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python环境
    pause
    exit /b 1
)

echo [2/5] 检查依赖...
pip show PyPDF2 >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装PyPDF2...
    pip install PyPDF2
)

pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
)

echo [3/5] 清理旧文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo [4/5] 开始打包...
pyinstaller --onefile --windowed --name="PDF拆分工具" --add-data="pdf_splitter.py;." pdf_splitter.py

echo [5/5] 检查打包结果...
if exist "dist\PDF拆分工具.exe" (
    echo.
    echo ==========================================
    echo             打包成功！
    echo ==========================================
    echo 输出文件：dist\PDF拆分工具.exe
    
    for %%I in ("dist\PDF拆分工具.exe") do (
        echo 文件大小：%%~zI 字节
    )
    
    echo.
    echo 是否要打开输出目录？[Y/N]
    set /p choice=
    if /i "%choice%"=="Y" (
        explorer "dist"
    )
) else (
    echo.
    echo ==========================================
    echo             打包失败！
    echo ==========================================
    echo 请检查错误信息并重试
)

echo.
pause