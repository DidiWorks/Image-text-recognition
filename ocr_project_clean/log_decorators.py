# log_decorators.py
import time
import functools
from typing import Callable, Any
from quality_logger import QualityLogger

def log_ocr_operation(logger: QualityLogger):
    """OCR操作日志装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                # 记录操作开始
                if args and hasattr(args[0], '__str__'):
                    logger.log_ocr_start(str(args[0]))
                
                # 执行函数
                result = func(*args, **kwargs)
                
                # 记录成功结果
                processing_time = time.time() - start_time
                logger.log_performance(func.__name__, processing_time)
                
                return result
                
            except Exception as e:
                # 记录错误
                error_msg = str(e)
                logger.log_ocr_error(str(args[0]) if args else "unknown", error_msg, type(e).__name__)
                raise
                
        return wrapper
    return decorator

def log_file_operation(logger: QualityLogger):
    """文件操作日志装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                
                # 记录文件生成
                if result and isinstance(result, str):
                    logger.log_file_generation("Generated", result)
                
                return result
                
            except Exception as e:
                logger.log_ocr_error("file_operation", str(e), type(e).__name__)
                raise
                
        return wrapper
    return decorator