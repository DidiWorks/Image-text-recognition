"""
配置管理模块
包含配置加载和格式注册功能
"""
import json
import os
from .formats.steel_quality import SteelQualityFormat
from .formats.generic_text import GenericTextFormat

# 格式注册表
FORMAT_REGISTRY = {
    "steel_quality_v1": SteelQualityFormat,
    "generic_v1": GenericTextFormat
}

def load_config(config_path="config/engine_config.json"):
    """加载配置文件"""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 返回默认配置
                    return {
            "current_ai_engine": "paddle",
            "current_format": "steel_quality_v1"
        }
    except Exception as e:
        return {}

def save_config(config, config_path="config/engine_config.json"):
    """保存配置文件"""
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False

def get_format(format_name):
    """获取格式处理器"""
    if format_name in FORMAT_REGISTRY:
        return FORMAT_REGISTRY[format_name]()
    else:
        raise ValueError(f"不支持的格式: {format_name}")

def register_format(format_name, format_class):
    """注册新格式"""
    FORMAT_REGISTRY[format_name] = format_class
