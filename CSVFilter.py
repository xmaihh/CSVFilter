import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox
from math import pow
from PIL import ImageTk, Image
import os
import sys

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


win = tk.Tk()
win.title("Wind Chill Index calculator")
# win.geometry('320x100')
win.geometry("500x300")


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

win.mainloop()
