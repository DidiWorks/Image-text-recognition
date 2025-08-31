"""
GUI 工具包
包含关键词管理、文本高亮、对比窗口等功能
"""

# 导入关键词管理功能
from .keywords_manager import (
    load_quality_keywords,
    save_quality_keywords,
    show_keywords_manager  
)

# 导入文本高亮功能
from .text_highlighter import (
    apply_highlighting,
    refresh_highlighting
)

# 导入对比窗口功能
from .compare_window import show_compare_window

# 导出所有公共接口
__all__ = [
    # 关键词管理
    'load_quality_keywords',
    'save_quality_keywords', 
    'show_keywords_manager',
    
    # 文本高亮
    'apply_highlighting',
    'refresh_highlighting',
    
    # 对比窗口
    'show_compare_window'
]