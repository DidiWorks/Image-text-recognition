"""
AI引擎模块
包含各种OCR引擎的实现
"""

from .paddle_engine import PaddleOCREngine

__all__ = [
    'PaddleOCREngine'
]
