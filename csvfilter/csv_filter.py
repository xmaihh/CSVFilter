import tkinter as tk
import os
from tkinter import filedialog
from . import helpers
import sys
import threading
import logging
from . import logger
import configparser


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.configure(state="disabled")
        self.text_widget.see(tk.END)


class CSVFilterApp:
    def __init__(self):
        my_logger = logger.MyLogger("csvfilter", "csvfilter.log")
        self.logger = my_logger.get_logger()
        self.root = self.createWindow()
        self.createWidget()
        text_handler = TextHandler(self.logpreview_text)
        text_handler.setLevel(logging.DEBUG)
        text_handler.setFormatter(my_logger.get_log_formatter())
        self.logger.addHandler(text_handler)
        self.input_file = ""
        self.output_file = ""

    def _get_resource_path(self, path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, path)
        return os.path.join(os.path.abspath("."), path)

    def createWindow(self):
        root = tk.Tk()
        root.title("CSV2XLSX Converter")
        root.iconbitmap(self._get_resource_path("resources/csv_filter.ico"))
        # 添加软件版本号标签
        config = configparser.ConfigParser()
        config.read(self._get_resource_path("config.ini"))
        print(self._get_resource_path("config.ini"))
        version = config.get("DEFAULT", "version")
        print(version)
        version_label = tk.Label(root, text=f"版本号：{version}")
        version_label.pack(side="bottom", pady=10)
        return root

    def createWidget(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        input_label = tk.Label(frame, text="输入路径：")
        input_label.grid(row=0, column=0, sticky="w", padx=10)

        self.input_entry = tk.Entry(frame, width=50)
        self.input_entry.grid(row=0, column=1)

        output_label = tk.Label(frame, text="输出路径:")
        output_label.grid(row=1, column=0, sticky="w", padx=10)

        self.output_entry = tk.Entry(frame, width=50)
        self.output_entry.grid(row=1, column=1)

        button_frame = tk.Frame(frame)
        button_frame.grid(row=2, column=1, sticky="e", pady=20)

        self.browse_button = tk.Button(
            button_frame, text="浏览...", command=self.browse_file
        )
        self.browse_button.pack(side="left")

        self.convert_button = tk.Button(
            button_frame,
            text="开始转换",
            bg="#ff6666",
            fg="#ffffff",
            command=self.start_conversion,
        )
        self.convert_button.pack(side="left", padx=10)

        # 添加日志预览文本框
        self.logpreview_text = tk.Text(self.root, height=10, width=50)
        self.logpreview_text.pack(padx=20, pady=10)

    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filepath:
            self.output_entry.delete(0, tk.END)
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(tk.END, filepath)
            self.input_entry.xview_moveto(1)
            self.input_file = filepath
            self.logger.info(f"输入路径：{filepath}")

    def start_conversion(self):
        if not os.path.isfile(self.input_file) or not os.access(
            self.input_file, os.R_OK
        ):
            self.logger.error(f"出错了，{self.input_file}不是有效的CSV文件")
            return ""
        self.output_entry.delete(0, tk.END)
        self.browse_button.config(state=tk.DISABLED)
        self.convert_button.config(state=tk.DISABLED, text="转换中...")
        self.logger.info(f"开始转换文件：{self.input_file} ->")

        def run_task():
            self.output_file = helpers.helper_function(self.input_file)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(tk.END, self.output_file)
            self.output_entry.xview_moveto(1)
            self.browse_button.config(state=tk.NORMAL)
            self.convert_button.config(state=tk.NORMAL, text="开始转换")
            self.logger.info(f"文件转换完成！{self.input_file} ===> {self.output_file}")

        thread = threading.Thread(target=run_task)
        thread.start()

    def run(self):
        self.root.mainloop()
