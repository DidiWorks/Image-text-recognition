"""
裁剪处理组件
负责区域选择、裁剪计算等功能
"""
from window_utils import ask_yes_no

class CropProcessor:
    """裁剪处理组件"""
    
    def __init__(self, image_display, event_handler):
        self.image_display = image_display
        self.event_handler = event_handler
        self.canvas = image_display.get_canvas()
        
        # 选择状态变量
        self.rect = None
        self.start_x = self.start_y = 0
        self.end_x = self.end_y = 0
        self.cropped_img = None
        self.should_proceed = False
    
    def start_selection(self, event):
        """开始选择区域"""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        img = self.image_display.get_displayed_image()
        img_width = img.width
        img_height = img.height
        
        # 确保坐标在图片范围内
        canvas_x = max(0, min(img_width, canvas_x))
        canvas_y = max(0, min(img_height, canvas_y))
        
        self.start_x, self.start_y = canvas_x, canvas_y
        
        # 删除之前的矩形
        if self.rect:
            self.canvas.delete(self.rect)
        
        # 创建新的选择矩形
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, 
            outline='red', width=2
        )
    
    def update_selection(self, event):
        """更新选择区域"""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        img = self.image_display.get_displayed_image()
        img_width = img.width
        img_height = img.height
        
        # 确保坐标在图片范围内
        canvas_x = max(0, min(img_width, canvas_x))
        canvas_y = max(0, min(img_height, canvas_y))
        
        self.end_x, self.end_y = canvas_x, canvas_y
        
        # 更新矩形位置
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
    
    def has_selection(self):
        """检查是否有选择区域"""
        return self.rect is not None
    
    def finish_selection(self):
        """完成选择并处理裁剪"""
        if not self.rect:
            return
        
        # 计算选择区域的边界
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        
        # 检查选择区域是否太小
        if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
            self.canvas.delete(self.rect)
            self.rect = None
            return
        
        # 计算裁剪坐标（转换到原始图片坐标系）
        scale_x = self.image_display.get_original_image().width / self.image_display.get_displayed_image().width
        scale_y = self.image_display.get_original_image().height / self.image_display.get_displayed_image().height
        
        crop_x1 = int(x1 * scale_x)
        crop_y1 = int(y1 * scale_y)
        crop_x2 = int(x2 * scale_x)
        crop_y2 = int(y2 * scale_y)
        
        # 执行裁剪
        self.cropped_img = self.image_display.get_original_image().crop((crop_x1, crop_y1, crop_x2, crop_y2))
        
        # 解绑事件
        self.event_handler.unbind_events()
        
        # 询问用户是否继续
        choice = ask_yes_no(
            "确认操作", 
            "已选择截图区域，是否进入文字识别对比？\n\n选择'是'：进入识别对比\n选择'否'：继续在图片上操作"
        )
        
        if choice:
            self.should_proceed = True
            # 获取主窗口并销毁
            main_window = self.canvas.winfo_toplevel()
            main_window.destroy()
        else:
            # 取消选择，重新绑定事件
            self.canvas.delete(self.rect)
            self.rect = None
            self.cropped_img = None
            self.event_handler.rebind_events()
    
    def get_cropped_image(self):
        """获取裁剪后的图片"""
        return self.cropped_img
    
    def should_proceed_to_ocr(self):
        """是否应该继续到OCR处理"""
        return self.should_proceed
