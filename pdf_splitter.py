import PyPDF2
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def get_resource_path(relative_path):
    """获取资源文件路径，支持打包后的exe"""
    try:
        # PyInstaller创建的临时文件夹
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def split_pdf_by_pages(input_path, pages_per_split=10, output_dir="split_pdfs"):
    """
    按指定页数拆分PDF
    
    Args:
        input_path: 输入PDF文件路径
        pages_per_split: 每个拆分文件的页数
        output_dir: 输出目录
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    # 打开PDF文件
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"原PDF总页数: {total_pages}")
        
        # 计算需要拆分的文件数
        num_splits = (total_pages + pages_per_split - 1) // pages_per_split
        print(f"将拆分为 {num_splits} 个文件")
        
        # 获取原文件名（不含扩展名）
        base_name = Path(input_path).stem
        
        # 开始拆分
        for i in range(num_splits):
            start_page = i * pages_per_split
            end_page = min((i + 1) * pages_per_split, total_pages)
            
            # 创建新的PDF写入器
            pdf_writer = PyPDF2.PdfWriter()
            
            # 添加页面到新PDF
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # 生成输出文件名
            output_filename = f"{base_name}_part_{i+1:03d}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # 写入新PDF文件
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"已创建: {output_filename} (页面 {start_page+1}-{end_page})")

def split_pdf_by_ranges(input_path, page_ranges, output_dir="split_pdfs"):
    """
    按指定页面范围拆分PDF
    
    Args:
        input_path: 输入PDF文件路径
        page_ranges: 页面范围列表，格式如 [(1, 5), (6, 10), (11, 15)]
        output_dir: 输出目录
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    # 打开PDF文件
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"原PDF总页数: {total_pages}")
        
        # 获取原文件名（不含扩展名）
        base_name = Path(input_path).stem
        
        # 按范围拆分
        for i, (start, end) in enumerate(page_ranges):
            # 验证页面范围
            if start < 1 or end > total_pages or start > end:
                print(f"跳过无效范围: {start}-{end}")
                continue
            
            # 创建新的PDF写入器
            pdf_writer = PyPDF2.PdfWriter()
            
            # 添加页面到新PDF（注意：页面索引从0开始）
            for page_num in range(start-1, end):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # 生成输出文件名
            output_filename = f"{base_name}_pages_{start}-{end}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # 写入新PDF文件
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"已创建: {output_filename} (页面 {start}-{end})")

def split_pdf_into_single_pages(input_path, output_dir="single_pages"):
    """
    将PDF拆分为单页文件
    
    Args:
        input_path: 输入PDF文件路径
        output_dir: 输出目录
    """
    # 创建输出目录
    Path(output_dir).mkdir(exist_ok=True)
    
    # 打开PDF文件
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"原PDF总页数: {total_pages}")
        
        # 获取原文件名（不含扩展名）
        base_name = Path(input_path).stem
        
        # 逐页拆分
        for page_num in range(total_pages):
            # 创建新的PDF写入器
            pdf_writer = PyPDF2.PdfWriter()
            
            # 添加当前页面
            pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # 生成输出文件名
            output_filename = f"{base_name}_page_{page_num+1:03d}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # 写入新PDF文件
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            print(f"已创建: {output_filename}")

class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF拆分工具")
        self.root.geometry("540x700")
        self.root.resizable(False, False)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.selected_file = tk.StringVar()
        self.output_dir = tk.StringVar(value="split_pdfs")
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件选择
        ttk.Label(main_frame, text="选择PDF文件:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(file_frame, textvariable=self.selected_file, width=50).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(file_frame, text="浏览", command=self.browse_file).grid(row=0, column=1)
        
        # 输出目录
        ttk.Label(main_frame, text="输出目录:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(output_frame, text="浏览", command=self.browse_output_dir).grid(row=0, column=1)
        
        # 拆分方式选择
        ttk.Label(main_frame, text="拆分方式:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        
        self.split_method = tk.StringVar(value="pages")
        
        # 单选按钮
        ttk.Radiobutton(main_frame, text="按页数拆分", variable=self.split_method, 
                       value="pages", command=self.on_method_change).grid(row=5, column=0, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(main_frame, text="按页面范围拆分", variable=self.split_method, 
                       value="ranges", command=self.on_method_change).grid(row=6, column=0, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(main_frame, text="拆分为单页", variable=self.split_method, 
                       value="single", command=self.on_method_change).grid(row=7, column=0, sticky=tk.W, pady=2)
        
        # 参数输入框架
        self.param_frame = ttk.LabelFrame(main_frame, text="参数设置", padding="10")
        self.param_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # 按页数拆分的参数
        self.pages_frame = ttk.Frame(self.param_frame)
        self.pages_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(self.pages_frame, text="每个文件包含页数:").grid(row=0, column=0, sticky=tk.W)
        self.pages_per_split = tk.StringVar(value="10")
        ttk.Entry(self.pages_frame, textvariable=self.pages_per_split, width=10).grid(row=0, column=1, padx=(10, 0))
        
        # 按范围拆分的参数
        self.ranges_frame = ttk.Frame(self.param_frame)
        ttk.Label(self.ranges_frame, text="页面范围 (格式: 1-5,6-10,11-15):").grid(row=0, column=0, sticky=tk.W)
        self.page_ranges = tk.StringVar()
        ttk.Entry(self.ranges_frame, textvariable=self.page_ranges, width=40).grid(row=1, column=0, pady=5)
        
        # 单页拆分的说明
        self.single_frame = ttk.Frame(self.param_frame)
        ttk.Label(self.single_frame, text="将每页拆分为单独的PDF文件", 
                 foreground="gray").grid(row=0, column=0, sticky=tk.W)
        
        # 默认显示按页数拆分的参数
        self.on_method_change()
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="开始拆分", command=self.start_split, 
                  style="Accent.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit).grid(row=0, column=1, padx=5)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="请选择PDF文件", foreground="blue")
        self.status_label.grid(row=11, column=0, columnspan=2, pady=5)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file.set(filename)
            self.status_label.config(text=f"已选择: {os.path.basename(filename)}")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)
    
    def on_method_change(self):
        # 隐藏所有参数框架
        for frame in [self.pages_frame, self.ranges_frame, self.single_frame]:
            frame.grid_remove()
        
        # 显示对应的参数框架
        method = self.split_method.get()
        if method == "pages":
            self.pages_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        elif method == "ranges":
            self.ranges_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        else:  # single
            self.single_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def start_split(self):
        if not self.selected_file.get():
            messagebox.showerror("错误", "请选择PDF文件")
            return
        
        if not os.path.exists(self.selected_file.get()):
            messagebox.showerror("错误", "选择的文件不存在")
            return
        
        try:
            self.progress.start()
            self.status_label.config(text="正在处理...")
            self.root.update()
            
            method = self.split_method.get()
            input_path = self.selected_file.get()
            output_dir = self.output_dir.get()
            
            if method == "pages":
                pages_per_split = int(self.pages_per_split.get())
                split_pdf_by_pages(input_path, pages_per_split, output_dir)
            elif method == "ranges":
                ranges_input = self.page_ranges.get()
                if not ranges_input:
                    messagebox.showerror("错误", "请输入页面范围")
                    return
                
                page_ranges = []
                for range_str in ranges_input.split(","):
                    start, end = map(int, range_str.strip().split("-"))
                    page_ranges.append((start, end))
                
                split_pdf_by_ranges(input_path, page_ranges, output_dir)
            else:  # single
                split_pdf_into_single_pages(input_path, output_dir)
            
            self.progress.stop()
            self.status_label.config(text="拆分完成！")
            messagebox.showinfo("成功", f"PDF拆分完成！\n输出目录: {output_dir}")
            
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="拆分失败")
            messagebox.showerror("错误", f"拆分失败: {str(e)}")

def main():
    root = tk.Tk()
    app = PDFSplitterGUI(root)
    root.mainloop()

# 使用示例
if __name__ == "__main__":
    main()