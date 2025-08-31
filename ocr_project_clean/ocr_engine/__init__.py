"""
OCR引擎模块
提供OCR识别、格式处理、配置管理等功能
"""

# 导入核心功能
from .core.ocr_processor import ocr_image
from .core.image_utils import check_image, convert_image

# 导入引擎
from .engines.paddle_engine import PaddleOCREngine

# 导入格式处理器
from .formats.steel_quality import SteelQualityFormat
from .formats.generic_text import GenericTextFormat

# 导入配置管理
from .config import load_config, save_config, get_format, register_format

# 导出主要接口
__all__ = [
    # 核心功能
    'ocr_image',
    'check_image',
    'convert_image',
    
    # 引擎
    'PaddleOCREngine',
    
    # 格式处理器
    'SteelQualityFormat',
    'GenericTextFormat',
    
    # 配置管理
    'load_config',
    'save_config',
    'get_format',
    'register_format'
]
