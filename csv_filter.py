import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
from math import pow
from PIL import ImageTk, Image
import os
import sys
from tkinter import filedialog
import pandas as pd

WindChillIndex = 0


def calc(temp, wind):
    if temp.get() == "":
        tkinter.messagebox.showerror("Error", "Temperature value error!")
        return ""

    if wind.get() == "":
        tkinter.messagebox.showerror("Error", "Wind speed value error!")
        return ""
    try:
        V016 = pow(float(wind.get()), 0.16)
        global WindChillIndex
        WindChillIndex = (
            13.12
            + (0.6215 * float(temp.get()))
            - (11.37 * V016)
            + (0.3965 * float(temp.get()) * V016)
        )
        ResultVar.set("WCI = " + str(round(WindChillIndex, 3)) + "°C")
    except Exception as identifier:
        tkinter.messagebox.showerror("Error", "Can not finish calculation!")


def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.xlsx")])
    if filepath:
        OpenFilePathLabel.config(text=filepath)

def filter_and_display():
    filepath = OpenFilePathLabel.cget("text")
    df = pd.read_csv(filepath)
    # 定义筛选条件
    condition = df["唯一标识imei"].str.startswith("86")
    # 根据筛选条件筛选数据
    df_filtered = df[condition]
    # 将筛选结果保存到新的 CSV 文件
    new_filepath = "filtered_" + filepath.split("/")[-1]

    if df_filtered.empty:  # 如果筛选结果为空
        print("没有符合条件的数据！")
        # 在这里你可以选择如何展示没有数据的提示
        # 比如使用 tkinter 的 Label 控件展示提示信息
        printLabel.config(text="没有符合条件的数据！")
    else:
        printLabel.config(text="有符合条件的数据！")
        df_filtered.to_csv(new_filepath, index=False)
        printLabel.config(text=new_filepath)
        # 在这里你可以选择如何展示筛选结果，比如使用 print()、展示在另一个窗口等方式
        print(df_filtered)


win = tk.Tk()
win.title("Wind Chill Index calculator")
# win.geometry('320x100')
win.geometry("600x500")


image = Image.open(get_resource_path("resources/windchill.png"))
image = image.resize((337, 20))  # 可选：调整图片大小
photo = ImageTk.PhotoImage(image)

tk.Label(win, text="The formula is:").grid(column=0, row=4, sticky="w", padx=10)
# 创建标签并显示图片
label = tk.Label(win, image=photo)
label.grid(column=0, row=5, padx=10)

# 設定標籤
tk.Label(win, text="Temperature:").grid(column=0, row=0, sticky="W", padx=10)

tempVar = tk.StringVar()
tempEntry = tk.Entry(win, width=20, textvariable=tempVar).grid(column=0, row=1, padx=10)

# 設定標籤
tk.Label(win, text="Wind Speed:").grid(column=0, row=2, sticky="w", padx=10)

windVar = tk.StringVar()
windEntry = tk.Entry(win, width=20, textvariable=windVar).grid(column=0, row=3, padx=10)

ResultVar = tk.StringVar()
ResultVar.set("WCI = None")
ResultLabel = tk.Label(
    win, textvariable=ResultVar, font=tkFont.Font(family="consolas", size=12)
).grid(column=1, row=1, padx=10)

CalcButton = tk.Button(
    win,
    text="Calculate",
    width=15,
    height=1,
    command=lambda temp=tempVar, wind=windVar: calc(temp, wind),
)
CalcButton.grid(column=1, row=3, padx=10)


# 选择要处理的csv文件
tk.Label(win, text="Open file:").grid(column=0, row=6, sticky="w", padx=10, pady=20)
OpenFileButton = tk.Button(win, text="选择文件", width=15, height=1, command=open_file)
OpenFileButton.grid(column=1, row=6, sticky="w", padx=10, pady=20)
OpenFilePathLabel = tk.Label(win, text="123")
OpenFilePathLabel.grid(column=0, row=7, sticky="w", padx=10)

# 筛选出86开头的含imei数据
Filter86Button = tk.Button(
    win, text="筛选并展示结果", width=15, height=1, command=filter_and_display
)
Filter86Button.grid(column=0, row=8, sticky="w", padx=10, pady=20)
printLabel = tk.Label(win, text="printf")
printLabel.grid(column=0, row=9, sticky="w", padx=10)


win.mainloop()
