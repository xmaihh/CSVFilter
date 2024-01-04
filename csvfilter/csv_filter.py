import tkinter as tk
import tkinter.messagebox
import os
import csv
from tkinter import filedialog
from . import helpers
import sys


class CSVFilterApp:
    def __init__(self):
        self.relative_path = "resources/csv_filter.ico"
        self.window = tk.Tk()
        self.window.title(f"CSV到XLSX转换器{helpers.get_git_version()}")
        self.window.iconbitmap(self._get_resource_path())
        self.createWidget()
        self.input_file = ""

    def _get_resource_path(self):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, self.relative_path)
        return os.path.join(os.path.abspath("."), self.relative_path)

    def createWidget(self):
        self.label_input_csv_file = tk.Label(self.window, text="输入路径：")
        self.entry_input_csv_file = tk.Entry(self.window, width=49)
        self.button_select_input_csv_file = tk.Button(
            self.window, text="选择", command=self.select_input_csv_file
        )
        self.button_start_conversion = tk.Button(
            self.window, text="开始转换", command=self.convert_to_excel_file
        )
        self.label_output_excel_file = tk.Label(self.window, text="输出路径：")
        self.entry_output_excel_file = tk.Entry(self.window, width=49)

        self.label_input_csv_file.grid(row=0, column=0, sticky="w")
        self.entry_input_csv_file.grid(row=0, column=1, padx=5, pady=5)
        self.button_select_input_csv_file.grid(row=0, column=2)
        self.button_start_conversion.grid(row=1, column=1, pady=10)
        self.label_output_excel_file.grid(row=2, column=0, sticky="w")
        self.entry_output_excel_file.grid(row=2, column=1, padx=5, pady=5)

    def select_input_csv_file(self):
        input_csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.input_file = input_csv_file
        self.entry_input_csv_file.delete(0, tk.END)  # 清空输入框
        self.entry_input_csv_file.insert(tk.END, input_csv_file)  # 将选择的路径插入到输入框中
        self.entry_input_csv_file.xview_moveto(1)  # 将文本框滚动到末尾
        self.entry_output_excel_file.delete(0, tk.END)

    def convert_to_excel_file(self):
        if not os.path.isfile(self.input_file) or not os.access(
            self.input_file, os.R_OK
        ):
            tkinter.messagebox.showerror("出错了", "无效的文件")
            return ""

        try:
            with open(self.input_file, "r", newline="") as f:
                dialect = csv.Sniffer().sniff(f.read(1024))
                f.seek(0)
                csv_reader = csv.reader(f, dialect)
                header = next(csv_reader)
        except (csv.Error, StopIteration):
            tkinter.messagebox.showerror("出错了", "不是有效的CSV文件")
            return ""

        output_excel_file = helpers.helper_function(self.input_file)
        self.entry_output_excel_file.delete(0, tk.END)
        self.entry_output_excel_file.insert(tk.END, output_excel_file)
        self.entry_output_excel_file.xview_moveto(1)

    def run(self):
        self.window.mainloop()
