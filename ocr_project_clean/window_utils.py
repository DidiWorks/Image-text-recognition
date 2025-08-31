# window_utils.py 窗口居中显示  创建标准窗口 状态栏进度条

import tkinter as tk
from tkinter import ttk
import time
import threading
from tkinter import messagebox as _mb
def center_window(window, width, height):
    """将窗口居中显示"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_standard_window(parent, title, width, height, modal=True):
    window = tk.Toplevel(parent)
    window.title(title)
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)

    if modal:
        window.transient(parent)
        window.grab_set()

    center_window(window, width, height)
    return window   

class OCRProgressPopup:
    def __init__(self, parent, title="OCR识别中", maximum=100):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x120")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        # 居中
        center_window(self.window, 400, 120)

        # 进度条 + 文本
        self.progress = ttk.Progressbar(self.window, maximum=maximum, length=350)
        self.progress.pack(pady=15)
        self.label = ttk.Label(self.window, text="")
        self.label.pack()

    def update_progress(self, value, text=""):
        self.progress["value"] = value
        if text:
            self.label.config(text=text)
        self.window.update()

    def close(self):
        self.window.destroy()

class ProgressAnimation:
    """进度条动画模块"""
    
    def __init__(self, parent, title="处理中", duration=3):
        self.parent = parent
        self.title = title
        self.duration = duration
        self.window = None
        self.progress = None
        self.label = None
        self.animation_thread = None
        self.is_running = False
    
    def show(self):
        """显示进度条窗口"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("400x120")
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # 居中
        center_window(self.window, 400, 120)
        
        # 进度条和标签
        self.progress = ttk.Progressbar(self.window, maximum=100, length=350)
        self.progress.pack(pady=15)
        self.label = tk.Label(self.window, text="正在处理...")
        self.label.pack()
        
        # 启动动画
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def _animate(self):
        """动画线程"""
        step_time = self.duration / 20  # 20步完成
        for i in range(0, 101, 5):
            if not self.is_running:
                break
            self.window.after(0, self._update_progress, i)
            time.sleep(step_time)
    
    def _update_progress(self, value):
        """更新进度条（在主线程中调用）"""
        if self.progress:
            self.progress["value"] = value
            self.window.update()
    
    def set_message(self, message):
        """设置消息文本"""
        if self.label:
            self.label.config(text=message)
            self.window.update()
    
    def close(self):
        """关闭进度条"""
        self.is_running = False
        if self.window:
            self.window.destroy()
            self.window = None

def show_progress_animation(parent, title="处理中", duration=3, message="正在处理..."):
    """快速显示进度条动画"""
    animation = ProgressAnimation(parent, title, duration)
    animation.show()
    animation.set_message(message)
    return animation

class StatusBar:
    def __init__(self, parent):
        self.label = ttk.Label(parent, relief=tk.SUNKEN, anchor="w")
        self.label.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self, text):
        self.label.config(text=text)

    def clear(self):
        self.label.config(text="")


def _wu_resolve_parent(parent=None):
    """ 弹窗窗口绑定"""
    if parent:
        return parent
    root = tk._default_root
    try:
        w = root.focus_get() 
        if w:
            return w.winfo_toplevel()
    except Exception:
        pass
    return root
def info(title, message, parent=None):
    return _mb.showinfo(title, message, parent=_wu_resolve_parent(parent))

def warn(title, message, parent=None):
    return _mb.showwarning(title, message, parent=_wu_resolve_parent(parent))

def error(title, message, parent=None):
    return _mb.showerror(title, message, parent=_wu_resolve_parent(parent))

def ask_yes_no(title, message, parent=None):
    return _mb.askyesno(title, message, parent=_wu_resolve_parent(parent))