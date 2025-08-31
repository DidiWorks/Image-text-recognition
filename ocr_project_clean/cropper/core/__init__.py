"""
截图核心功能模块
提供截图器的基础功能和工具
"""

# 导入核心功能
from .image_display import ImageDisplay
from .event_handler import EventHandler
from .crop_processor import CropProcessor

# 导出主要接口
__all__ = [
    # 核心组件
    'ImageDisplay',
    'EventHandler', 
    'CropProcessor',
]
