"""
增强截图器模块
使用组件化架构，提供图片区域选择、缩放、裁剪等交互功能
"""
import tkinter as tk
from window_utils import center_window
from .core import ImageDisplay, EventHandler, CropProcessor

class EnhancedCropper(tk.Toplevel):
    """增强截图器主类"""
    
    def __init__(self, image_path):
        super().__init__()
        self.title("选择识别区域 (左键拖动截图,右键复制照片,Ctrl+滚轮缩放)")
        self.geometry("1200x800")
        self.minsize(800, 600)
        center_window(self, 1200, 800)
        
        # 初始化组件
        self.image_display = ImageDisplay(self, image_path)
        self.crop_processor = CropProcessor(self.image_display, None)  # 临时设为None
        self.event_handler = EventHandler(self.image_display, self.crop_processor)
        
        # 更新crop_processor的event_handler引用
        self.crop_processor.event_handler = self.event_handler
        
        # 设置结果变量
        self.cropped_img = None
        self.should_proceed = False

def select_and_crop_enhanced(image_path):
    """弹出增强的截图窗口，让用户选择识别区域，返回裁剪后的PIL.Image对象"""
    root = tk.Tk()
    root.withdraw()
    cropper = EnhancedCropper(image_path)
    cropper.wait_window()
    
    if cropper.crop_processor.should_proceed_to_ocr():
        return cropper.crop_processor.get_cropped_image()
    else:
        return None
