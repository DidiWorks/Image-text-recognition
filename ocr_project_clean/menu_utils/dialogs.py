"""
对话框模块
包含各种设置和配置对话框
"""
import tkinter as tk
from tkinter import ttk
from window_utils import center_window
from .config import load_config, save_config
from ocr_engine.engines.factory import list_engines
from ocr_engine.formats.factory import list_formats



def show_about(root):
    """显示关于页面"""
    about_window = tk.Toplevel(root)
    about_window.title("关于")
    about_window.geometry("300x250")
    about_window.resizable(False, False)
    
    about_window.transient(root)
    about_window.grab_set()
    about_window.lift(); about_window.focus_force() 
   
    
    # 主框架
    main_frame = tk.Frame(about_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # 信息框架
    info_frame = tk.Frame(main_frame)
    info_frame.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(info_frame, text="OCR文字识别工具", font=("Arial", 16, "bold")).pack(pady=(0,10))
    tk.Label(info_frame, text="版本: 1.0.0").pack(pady=2)
    tk.Label(info_frame, text="开发: 二级计算机").pack(pady=2)
    tk.Label(info_frame, text="功能: 图像文字识别").pack(pady=2)
    tk.Label(info_frame,text="维护电话： 15xxxxx213").pack(pady=(0,10))

    # 按钮框架
    button_frame = tk.Frame(main_frame)
    button_frame.pack(side=tk.BOTTOM, pady=10)
    
    # 标准尺寸的按钮
    tk.Button(button_frame, text="确定", command=about_window.destroy,
              width=8, height=1, font=("Arial", 10)).pack()
    
def show_recognition_settings(root):
    """显示识别设置对话框"""
    config = load_config()
    
    #创建设置窗口
    settings_window = tk.Toplevel(root)
    settings_window.title("识别设置")
    settings_window.geometry("400x280")
    settings_window.resizable(False,False)
    settings_window.transient(root)
    settings_window.grab_set()
    settings_window.lift()
    settings_window.focus_force()

    #主框架
    main_frame = tk.Frame(settings_window, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    #标题
    title_label = tk.Label(main_frame, text="识别引擎与格式设置", font=("Arial", 14, "bold"))
    title_label.pack(pady=(0,20))

    #引擎选择区域
    engine_frame = tk.Frame(main_frame)
    engine_frame.pack(fill=tk.X, pady=(0,15))

    tk.Label(engine_frame, text="选择识别引擎：", font=("Arial", 11, "bold")).pack(anchor='w')    
    engine_var = tk.StringVar(value=config.get("engine", {}).get("current", "paddle"))
    engine_cb = ttk.Combobox(engine_frame, textvariable=engine_var,
                             values=list_engines(), state="readonly", width=30)
    engine_cb.pack(fill='x', pady=(5,0))

     # 格式选择区域
    format_frame = tk.Frame(main_frame)
    format_frame.pack(fill=tk.X, pady=(0, 20))
    
    tk.Label(format_frame, text="选择输出格式：", font=("Arial", 11, "bold")).pack(anchor='w')
    format_var = tk.StringVar(value=config.get("format", {}).get("current", "steel_quality_v1"))
    format_cb = ttk.Combobox(format_frame, textvariable=format_var,
                            values=list_formats(), state="readonly", width=30)
    format_cb.pack(fill='x', pady=(5, 0))

    #说明文字
    info_label = tk.Label(main_frame, text="说明：设置将在下次识别时生效",
                          font=("Arial", 9), fg="gray")
    info_label.pack(pady=(0,15))
  
    # 按钮区域
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.X)
    
    def save_settings():
        """保存设置到配置文件"""
        try:
            # 更新配置
            if "engine" not in config:
                config["engine"] = {}
            if "format" not in config:
                config["format"] = {}
                
            config["engine"]["current"] = engine_var.get()
            config["format"]["current"] = format_var.get()
            
            # 保存到文件
            save_config(config)
            
            # 显示成功消息
            from window_utils import info
            info("保存成功", "识别设置已保存，将在下次识别时生效", parent=settings_window)
            
            settings_window.destroy()
            
        except Exception as e:
            from window_utils import error
            error("保存失败", f"保存设置时发生错误：{str(e)}", parent=settings_window)
    
    def cancel_settings():
        """取消设置"""
        settings_window.destroy()
    
    # 保存按钮
    save_btn = tk.Button(button_frame, text="保存设置", command=save_settings,
                        bg="blue", fg="white", width=12, height=2, font=("Arial", 11))
    save_btn.pack(side=tk.RIGHT, padx=(10, 0))
    
    # 取消按钮
    cancel_btn = tk.Button(button_frame, text="取消", command=cancel_settings,
                          width=12, height=2, font=("Arial", 11))
    cancel_btn.pack(side=tk.RIGHT)
    
    # 居中显示
    settings_window.update_idletasks()
    center_window(settings_window, 400, 280)
