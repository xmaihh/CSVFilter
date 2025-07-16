# PDF拆分工具 - PyInstaller打包指南

## 1. 环境准备

### 安装依赖
```bash
pip install PyPDF2 pyinstaller
```

### 文件结构
```
pdf_splitter/
├── pdf_splitter.py       # 主程序文件
├── requirements.txt      # 依赖文件
├── build_spec.py         # 打包配置生成脚本
└── pdf_splitter.spec     # PyInstaller配置文件（自动生成）
```

## 2. 创建requirements.txt

```txt
PyPDF2==3.0.1
```

## 3. 打包步骤

### 方法一：直接打包（推荐）
```bash
# 生成单个exe文件，无控制台窗口
pyinstaller --onefile --windowed --name="PDF拆分工具" --icon=icon.ico pdf_splitter.py

# 如果没有图标文件，可以省略--icon参数
pyinstaller --onefile --windowed --name="PDF拆分工具" pdf_splitter.py
```

### 方法二：使用spec文件（更精细控制）
```bash
# 1. 生成spec文件
pyinstaller --onefile --windowed pdf_splitter.py

# 2. 编辑pdf_splitter.spec文件（可选）
# 3. 使用spec文件打包
pyinstaller pdf_splitter.spec
```

## 4. 打包参数说明

| 参数 | 说明 |
|------|------|
| `--onefile` | 打包成单个exe文件 |
| `--windowed` | 无控制台窗口（GUI程序） |
| `--console` | 有控制台窗口（调试用） |
| `--name` | 指定exe文件名 |
| `--icon` | 指定图标文件 |
| `--add-data` | 添加数据文件 |
| `--hidden-import` | 添加隐藏导入 |
| `--exclude-module` | 排除模块 |

## 5. 优化打包大小

### 排除不必要的模块
```bash
pyinstaller --onefile --windowed \
  --exclude-module matplotlib \
  --exclude-module numpy \
  --exclude-module PIL \
  pdf_splitter.py
```

### 使用UPX压缩（可选）
```bash
# 安装UPX
# Windows: 下载UPX并添加到PATH
# Linux: apt-get install upx

pyinstaller --onefile --windowed --upx-dir=/path/to/upx pdf_splitter.py
```

## 6. 常见问题解决

### 问题1：ModuleNotFoundError
```bash
# 添加隐藏导入
pyinstaller --onefile --windowed --hidden-import=tkinter pdf_splitter.py
```

### 问题2：文件路径问题
代码中已包含 `get_resource_path()` 函数来处理资源文件路径问题。

### 问题3：打包后exe文件过大
- 使用虚拟环境，只安装必要的包
- 排除不必要的模块
- 使用UPX压缩

### 问题4：杀毒软件误报
- 在杀毒软件中添加信任
- 使用代码签名证书

## 7. 完整打包脚本

创建 `build.bat` (Windows) 或 `build.sh` (Linux/Mac)：

### Windows (build.bat)
```batch
@echo off
echo 开始打包PDF拆分工具...

rem 清理旧文件
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

rem 打包
pyinstaller --onefile --windowed --name="PDF拆分工具" pdf_splitter.py

rem 检查结果
if exist "dist\PDF拆分工具.exe" (
    echo 打包成功！
    echo 输出文件：dist\PDF拆分工具.exe
    pause
) else (
    echo 打包失败！
    pause
)
```

### Linux/Mac (build.sh)
```bash
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
```

## 8. 测试打包结果

1. 在不同的机器上测试exe文件
2. 测试所有功能是否正常
3. 检查文件大小是否合理
4. 确认启动速度

## 9. 分发准备

### 创建安装包（可选）
使用 NSIS、Inno Setup 等工具创建安装程序。

### 文件说明
创建 `README.txt`：
```
PDF拆分工具 v1.0

功能：
- 按页数拆分PDF
- 按页面范围拆分PDF  
- 拆分为单页PDF

使用方法：
1. 运行 PDF拆分工具.exe
2. 选择要拆分的PDF文件
3. 选择拆分方式和参数
4. 点击"开始拆分"

注意事项：
- 支持所有标准PDF文件
- 输出文件保存在指定目录
- 程序无需安装，直接运行
```

## 10. 最终目录结构

```
pdf_splitter/
├── pdf_splitter.py       # 源代码
├── requirements.txt      # 依赖列表
├── build.bat            # Windows打包脚本
├── build.sh             # Linux/Mac打包脚本
├── README.txt           # 使用说明
└── dist/                # 打包输出目录
    └── PDF拆分工具.exe   # 最终可执行文件
```

运行打包脚本后，在 `dist` 目录下就能找到打包好的单个exe文件，可以直接分发给用户使用。