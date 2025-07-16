#!/bin/bash
echo "开始打包PDF拆分工具..."

# 清理旧文件
rm -rf dist build *.spec

# 打包
pyinstaller --onefile --windowed --name="PDF拆分工具" pdf_splitter.py

# 检查结果
if [ -f "dist/PDF拆分工具" ]; then
    echo "打包成功！"
    echo "输出文件：dist/PDF拆分工具"
else
    echo "打包失败！"
fi