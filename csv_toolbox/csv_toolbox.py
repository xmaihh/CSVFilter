import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk
from csv_toolbox import helpers
import sys
import threading
import logging
from csv_toolbox.lib_log.logger import MyLogger
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
        my_logger = MyLogger("csvfilter", "csvfilter.log")
        self.logger = my_logger.get_logger()
        self.root = self.createWindow()
        self.imei_filter_var = tk.StringVar(value="exclude")
        self.mac_filter_var = tk.StringVar(value="exclude")
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
        input_label.grid(row=0, column=0, sticky="w", padx=5)

        self.input_entry = tk.Entry(frame, width=50)
        self.input_entry.grid(row=0, column=1)

        output_label = tk.Label(frame, text="输出路径:")
        output_label.grid(row=1, column=0, sticky="w", padx=5)

        self.output_entry = tk.Entry(frame, width=50)
        self.output_entry.grid(row=1, column=1)

        # 添加分割线
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # 添加筛选
        self.create_filter_frame(frame)

        button_frame = tk.Frame(frame)
        button_frame.grid(row=6, column=1, columnspan=3, sticky="e", pady=20)

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
        self.logpreview_text = tk.Text(self.root, height=10, width=90)
        self.logpreview_text.pack(padx=20, pady=5)

    def create_filter_frame(self, master):
        self.filter_frame = master

        self.imei_label = tk.Label(self.filter_frame, text="输入 IMEI：")
        self.imei_label.grid(row=3, column=0, sticky="w", padx=5)

        self.imei_entry = tk.Entry(self.filter_frame, width=50)
        self.imei_entry.grid(row=3, column=1)

        self.imei_radio_frame = tk.Frame(self.filter_frame)
        self.imei_include = tk.Radiobutton(
            self.imei_radio_frame,
            text="包含",
            variable=self.imei_filter_var,
            value="include",
            command=self.on_imei_radio_select,
        )
        self.imei_include.pack(side="left")

        self.imei_exclude = tk.Radiobutton(
            self.imei_radio_frame,
            text="排除",
            variable=self.imei_filter_var,
            value="exclude",
            command=self.on_imei_radio_select,
        )
        self.imei_exclude.pack(side="left")
        self.imei_radio_frame.grid(row=3, column=2)

        self.mac_label = tk.Label(self.filter_frame, text="输入 MAC：")
        self.mac_label.grid(row=4, column=0, sticky="w", padx=5)

        self.mac_entry = tk.Entry(self.filter_frame, width=50)
        self.mac_entry.grid(row=4, column=1)

        self.mac_radio_frame = tk.Frame(self.filter_frame)
        self.mac_include = tk.Radiobutton(
            self.mac_radio_frame,
            text="包含",
            variable=self.mac_filter_var,
            value="include",
            command=self.on_mac_radio_select,
        )
        self.mac_include.pack(side="left")

        self.mac_exclude = tk.Radiobutton(
            self.mac_radio_frame,
            text="排除",
            variable=self.mac_filter_var,
            value="exclude",
            command=self.on_mac_radio_select,
        )
        self.mac_exclude.pack(side="left")
        self.mac_radio_frame.grid(row=4, column=2)

        text = """请根据需要输入 IMEI 和 MAC 的值。以下是输入示例：

        如果您选择了 "排除" 选项：
            IMEI：输入要从 CSV 文件中排除的 IMEI 值，多个值之间用空格分隔。例如：12345678 98765432。
            MAC：输入要从 CSV 文件中排除的 MAC 值，多个值之间用空格分隔。例如：00:11:22:33:44:55 66:77:88:99:aa:bb。

        如果您选择了 "包含" 选项：
            IMEI：输入要在 CSV 文件中包含的 IMEI 值，多个值之间用空格分隔。例如：12345678 98765432。
            MAC：输入要在 CSV 文件中包含的 MAC 值，多个值之间用空格分隔。例如：00:11:22:33:44:55 66:77:88:99:aa:bb。

请注意，在输入 IMEI 和 MAC 时，使用空格将多个值分隔开。"""

        self.instructions_label = tk.Label(
            self.filter_frame, text=text, justify=tk.LEFT, foreground="gray"
        )
        self.instructions_label.grid(row=5, column=0, columnspan=100)

    def on_imei_radio_select(self):
        """IMEI 选择改变时的处理函数"""
        imei_filter = self.imei_filter_var.get()
        imeis = self.imei_entry.get().strip().split()
        self.logger.info(f"IMEI Filter: {imei_filter} = {imeis}")

    def on_mac_radio_select(self):
        """MAC 选择改变时的处理函数"""
        mac_filter = self.mac_filter_var.get()
        macs = self.mac_entry.get().strip().split()
        self.logger.info(f"MAC Filter: {mac_filter} = {macs}")

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
        if not os.path.isfile(self.input_file):
            self.logger.error(f"请选择一个.csv文件…")
            return

        if not os.access(self.input_file, os.R_OK):
            self.logger.error(f"出错了，{self.input_file}不是有效的CSV文件")
            return
        self.output_entry.delete(0, tk.END)
        self.browse_button.config(state=tk.DISABLED)
        self.convert_button.config(state=tk.DISABLED, text="转换中...")
        self.logger.info(f"开始转换文件：{self.input_file} ->")

        def run_task():
            imei_filter = self.imei_filter_var.get()
            imeis = self.imei_entry.get().strip().split()
            self.logger.info(f"IMEI Filter: {imei_filter} = {imeis}")
            mac_filter = self.mac_filter_var.get()
            macs = self.mac_entry.get().strip().split()
            self.logger.info(f"MAC Filter: {mac_filter} = {macs}")
            self.output_file = helpers.helper_function(
                self.input_file,
                filter_imeis=imeis,
                filter_imei_include=imei_filter == "include",
                filter_macs=macs,
                filter_mac_include=mac_filter == "include",
            )
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
