"""
配置管理模块
负责配置文件的读取、保存和默认值管理
"""
import json
import os

SETTINGS_PATH = "config/settings.json"

def load_config():
    """读取配置文件"""
    config_path = "config/settings.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                loaded_config = json.load(f)
                # 确保配置包含所有必要的键
                default_config = get_default_config()
                # 合并配置，确保所有键都存在
                for key in default_config:
                    if key not in loaded_config:
                        loaded_config[key] = default_config[key]
                return loaded_config
        except Exception as e:
            return get_default_config()
    return get_default_config()

def save_config(config):
    """保存配置文件"""
    os.makedirs("config", exist_ok=True)
    with open("config/settings.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_default_config():
    """精简配置 - 只保留核心功能"""
    return {
        "app": {
            "name": "OCR识别工具",
            "version": "1.0.0"
        },
        "ocr": {
            "confidence_threshold": 0.8,
            "lang": "ch"
        }
    }
