# 日志系统
import logging
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any
import json

class QualityLogger:
    """轻量级质量数据记录日志系统"""
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        """
        初始化日志系统
        
        Args:
            log_dir: 日志文件存储目录
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_dir = log_dir
        self.setup_logging(log_level)
        
    def setup_logging(self, log_level: str):
        """设置日志配置"""
        # 创建日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
                #移除所有已存在得handler
        for h in logging.root.handlers[:]:
            logging.root.removeHandler(h)


        # 设置日志格式
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'


        # 配置日志
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            datefmt=date_format,
            handlers=[
                # 控制台输出
                logging.StreamHandler(),
                # 文件输出 - 按日期分割
                logging.FileHandler(
                    os.path.join(self.log_dir, f"quality_{datetime.now().strftime('%Y%m%d')}.log"),
                    encoding='utf-8'
                )
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def log_ocr_start(self, image_path: str, image_info: Dict[str, Any] = None):
        """记录OCR开始处理"""
        info = {
            "image_path": image_path,
            "timestamp": datetime.now().isoformat(),
            "image_info": image_info or {}
        }
        self.logger.info(f"OCR处理开始: {json.dumps(info, ensure_ascii=False)}")
        
    def log_ocr_result(self, image_path: str, result: str, confidence: float = None, 
                      processing_time: float = None):
        """记录OCR识别结果"""
        info = {
            "image_path": image_path,
            "result": result,
            "confidence": confidence,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"OCR识别结果: {json.dumps(info, ensure_ascii=False)}")
        
    def log_ocr_error(self, image_path: str, error_msg: str, error_type: str = None):
        """记录OCR错误"""
        info = {
            "image_path": image_path,
            "error_msg": error_msg,
            "error_type": error_type,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.error(f"OCR处理错误: {json.dumps(info, ensure_ascii=False)}")
        
    def log_data_validation(self, original_data: str, ocr_data: str, is_valid: bool, 
                          validation_notes: str = None):
        """记录数据验证结果"""
        info = {
            "original_data": original_data,
            "ocr_data": ocr_data,
            "is_valid": is_valid,
            "validation_notes": validation_notes,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"数据验证: {json.dumps(info, ensure_ascii=False)}")
        
    def log_file_generation(self, file_type: str, file_path: str, content_summary: str = None):
        """记录文件生成"""
        info = {
            "file_type": file_type,
            "file_path": file_path,
            "content_summary": content_summary,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"文件生成: {json.dumps(info, ensure_ascii=False)}")


    def log_performance(self, operation: str, duration: float, details: Dict[str, Any] = None):
        """记录性能指标"""
        info = {
            "operation": operation,
            "duration": duration,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"性能监控: {json.dumps(info, ensure_ascii=False)}")
        
    def log_daily_summary(self, date: str, total_images: int, success_count: int, 
                         error_count: int, total_processing_time: float):
        """记录每日总结"""
        summary = {
            "date": date,
            "total_images": total_images,
            "success_count": success_count,
            "error_count": error_count,
            "success_rate": success_count / total_images if total_images > 0 else 0,
            "total_processing_time": total_processing_time,
            "avg_processing_time": total_processing_time / total_images if total_images > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }
        self.logger.info(f"每日总结: {json.dumps(summary, ensure_ascii=False)}")

