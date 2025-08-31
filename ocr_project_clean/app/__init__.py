"""
应用层模块
负责装配 GUI、业务流程与日志。
"""

# 对外导出 run_app
from .app import run_app

__all__ = [
    'run_app',
]


