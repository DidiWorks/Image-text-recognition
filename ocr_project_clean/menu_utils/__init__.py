"""
菜单引擎模块
提供菜单创建、设置对话框、配置管理等功能
"""

# 导入核心功能
from .config import load_config, save_config, get_default_config
from .menu_bar import create_menu_bar
from .dialogs import  show_about, show_recognition_settings

# 导出主要接口
__all__ = [
    # 配置管理
    'load_config',
    'save_config', 
    'get_default_config',
    
    # 菜单创建
    'create_menu_bar',
    
    # 对话框

    'show_about',
    'show_recognition_settings'
]
