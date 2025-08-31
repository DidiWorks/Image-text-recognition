"""
事件处理组件
负责鼠标事件、键盘事件的处理
"""
import tkinter as tk

class EventHandler:
    """事件处理组件"""
    
    def __init__(self, image_display, crop_processor):
        self.image_display = image_display
        self.crop_processor = crop_processor
        self.canvas = image_display.get_canvas()
        
        # 拖拽状态变量
        self.is_dragging = False
        self.has_dragged = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.scroll_x = 0
        self.scroll_y = 0
        
        # 绑定事件
        self._bind_events()
    
    def _bind_events(self):
        """绑定所有事件"""
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.copy_image)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
    
    def on_mousewheel(self, event):
        """鼠标滚轮事件处理"""
        if event.state & 0x0004:  # Ctrl键
            self._handle_zoom(event)
            return "break"
        elif event.state & 0x0001:  # Shift键
            self._handle_horizontal_scroll(event)
            return "break"
        else:
            self._handle_vertical_scroll(event)
            return "break"
    
    def _handle_zoom(self, event):
        """处理缩放"""
        old_mouse_x = self.canvas.canvasx(event.x)
        old_mouse_y = self.canvas.canvasy(event.y)
        old_scale = self.image_display.get_scale_factor()
        
        if event.delta > 0:
            new_scale = old_scale * 1.1
        else:
            new_scale = old_scale / 1.1
        
        new_scale = max(0.2, min(5.0, new_scale))
        self.image_display.set_scale_factor(new_scale)
        
        # 调整滚动位置以保持鼠标位置不变
        scale_ratio = new_scale / old_scale
        new_mouse_x = old_mouse_x * scale_ratio
        new_mouse_y = old_mouse_y * scale_ratio
        
        delta_x = new_mouse_x - old_mouse_x
        delta_y = new_mouse_y - old_mouse_y
        
        current_scroll_x = self.canvas.xview()[0]
        current_scroll_y = self.canvas.yview()[0]
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img = self.image_display.get_displayed_image()
        
        scroll_ratio_x = delta_x / max(1, img.width - canvas_width)
        scroll_ratio_y = delta_y / max(1, img.height - canvas_height)
        
        new_scroll_x = max(0, min(1, current_scroll_x + scroll_ratio_x))
        new_scroll_y = max(0, min(1, current_scroll_y + scroll_ratio_y))
        
        self.canvas.xview_moveto(new_scroll_x)
        self.canvas.yview_moveto(new_scroll_y)
    
    def _handle_horizontal_scroll(self, event):
        """处理水平滚动"""
        scroll_step = int(event.delta / 120)
        current_scroll_x = self.canvas.xview()[0]
        canvas_width = self.canvas.winfo_width()
        img = self.image_display.get_displayed_image()
        
        if img.width > canvas_width:
            scroll_ratio_x = scroll_step * 0.1
            new_scroll_x = max(0, min(1, current_scroll_x - scroll_ratio_x))
            self.canvas.xview_moveto(new_scroll_x)
    
    def _handle_vertical_scroll(self, event):
        """处理垂直滚动"""
        scroll_step = int(event.delta / 120)
        current_scroll_y = self.canvas.yview()[0]
        canvas_height = self.canvas.winfo_height()
        img = self.image_display.get_displayed_image()
        
        if img.height > canvas_height:
            scroll_ratio_y = scroll_step * 0.1
            new_scroll_y = max(0, min(1, current_scroll_y - scroll_ratio_y))
            self.canvas.yview_moveto(new_scroll_y)
    
    def copy_image(self, event):
        """复制图片到剪贴板"""
        try:
            import io            
            output = io.BytesIO()
            self.image_display.get_original_image().convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]
            output.close()
            
            self.canvas.clipboard_clear()
            self.canvas.clipboard_append(data)
        except Exception as e:
            pass

    def on_press(self, event):
        """鼠标按下事件"""
        if event.state & 0x0004:  # Ctrl键被按下
            self.is_dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.scroll_x = self.canvas.xview()[0]
            self.scroll_y = self.canvas.yview()[0]
        else:
            self.is_dragging = False
            self.has_dragged = False
            self.crop_processor.start_selection(event)

    def on_drag(self, event):
        """鼠标拖拽事件"""
        if self.is_dragging:
            self._handle_canvas_drag(event)
        else:
            self.has_dragged = True
            self.crop_processor.update_selection(event)

    def _handle_canvas_drag(self, event):
        """处理画布拖拽"""
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        x_move = -dx / canvas_width
        y_move = -dy / canvas_height
        
        new_scroll_x = max(0, min(1, self.scroll_x + x_move))
        new_scroll_y = max(0, min(1, self.scroll_y + y_move))
        
        self.canvas.xview_moveto(new_scroll_x)
        self.canvas.yview_moveto(new_scroll_y)

    def on_release(self, event):
        """鼠标释放事件"""
        if not self.is_dragging and self.crop_processor.has_selection() and self.has_dragged:
            self.crop_processor.finish_selection()
        self.is_dragging = False
    
    def unbind_events(self):
        """解绑所有事件"""
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Button-3>")
        self.canvas.unbind("<MouseWheel>")
    
    def rebind_events(self):
        """重新绑定事件"""
        self._bind_events()
