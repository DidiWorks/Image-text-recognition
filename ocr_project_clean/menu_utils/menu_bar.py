"""
菜单栏创建模块
负责创建主菜单栏和菜单项
"""
import tkinter as tk
from .dialogs import show_excel_settings, show_about, show_recognition_settings

def create_menu_bar(root, select_and_recognize_func):
    """创建精简菜单栏"""
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # 工具菜单 - 只保留Excel功能
    tools_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="工具", menu=tools_menu)
    tools_menu.add_command(label="Excel设置", command=lambda: show_excel_settings(root))
    tools_menu.add_command(label="识别设置", command=lambda: show_recognition_settings(root))

    # 帮助菜单
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="帮助", menu=help_menu)
    help_menu.add_command(label="关于", command=lambda: show_about(root))
    
    return menubar
