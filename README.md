
# 操作命令

```
.\venv\Scripts\activate.ps1
pip install  pyinstaller
pip install pillow
pyinstaller -F --add-data "resources/*.png;resources/" --icon=.\resources\csv_filter.ico -w --debug all CSVFilter.py
```

# 生成requirements.txt文件

1. pip-tools管理依赖

```
pip install pip-tools
```

2. 创建 `requirements.in` 文件

创建一个 requirements.in 文件，并且只包含项目的直接依赖项。每次您想要更新或包含依赖项时，都必须先修改 requirements.in 。它与 requirements.txt 的区别也很明显，那就是只包含直接依赖的库，也可以指定版本,编译 requirements.in 可以直接生成 requirements.txt，但是你会发现这个 requirements.txt 跟 pip freeze 生成的有很大不同，你可以看到某个包是通过那个包引入的，依赖关系一目了然。

```
pip-compile requirements.in
```

3. 升级包

以 Django 为例：

```
pip-compile --upgrade-package django
```

这将自动更新您的 requirements.txt 文件，包括依赖项的修改。

4. 同步包

为了使 virtualenv 与当前的 requirements.txt 文件同步，您可以简单地运行以下命令：

```
pip-sync -a requirements.txt
```

这将先询问，当你输入 y 时，会在虚拟环境中安装、升级或卸载，最终与 requirements.txt 文件包含的包保持一致。

# 打包成.exe

```
 pyinstaller -F --add-data "resources/*.png;resources/" --icon=.\resources\csv_filter.ico -w --debug all CSVFilter.py
```

# 项目文件夹遵循以下结构:

https://waterprogramming.wordpress.com/2023/01/18/structuring-a-python-project-recommendations-and-a-template-example/

```
example_python_project/ 
├── sample_package/ 
│   ├── subpackage/ 
│   │   ├── __init__.py 
│   │   └── subpackage_module.py 
│   ├── __init__.py 
│   ├── helpers.py 
│   └── module.py 
├── docs/ 
│   └── documentation.md 
├── tests/ 
│   ├── __init__.py 
│   └── basic_test.py 
├── main.py 
├── README.md 
├── requirements.txt 
└── LICENSE
```