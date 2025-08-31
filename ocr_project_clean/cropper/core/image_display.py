"""
图片显示组件
负责图片的加载、缩放、显示等功能
"""
import tkinter as tk
from PIL import Image, ImageTk
from window_utils import center_window

class ImageDisplay:
    """图片显示组件"""
    
    def __init__(self, parent, image_path):
        self.parent = parent
        self.original_img = Image.open(image_path)
        self.img = self.original_img.copy()
        self.scale_factor = 1.0
        self.tk_img = None
        
        # 创建主框架
        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # 创建画布框架
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(expand=True, fill=tk.BOTH)

        # 创建画布
        self.canvas = tk.Canvas(self.canvas_frame, bg='gray', highlightthickness=0)
        
        # 创建滚动条
        self.hbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        # 配置画布滚动
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        # 布局滚动条和画布
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 显示图片
        self.update_display()
    
    def update_display(self):
        """更新图片显示"""
        new_width = int(self.original_img.width * self.scale_factor)
        new_height = int(self.original_img.height * self.scale_factor)
        self.img = self.original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(self.img)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
    
    def get_canvas(self):
        """获取画布对象"""
        return self.canvas
    
    def get_scale_factor(self):
        """获取当前缩放因子"""
        return self.scale_factor
    
    def set_scale_factor(self, factor):
        """设置缩放因子"""
        self.scale_factor = factor
        self.update_display()
    
    def get_original_image(self):
        """获取原始图片"""
        return self.original_img
    
    def get_displayed_image(self):
        """获取当前显示的图片"""
        return self.img
