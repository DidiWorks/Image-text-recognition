"""
OCR处理主逻辑
"""
import time
from menu_utils import load_config
from ..engines.factory import get_engine
from ..formats.factory import get_format

def ocr_image(image_input, format_name=None):
    """主OCR处理函数"""
    start_time = time.time()
    
    try:
        # 加载配置
        config = load_config()
        
        # 读取当前引擎/格式名（兼容多种配置格式）
        engine_name = (config.get("engine", {}).get("current")
                      or config.get("current_ai_engine")
                      or "paddle")
        format_name = (config.get("format", {}).get("current")
                      or config.get("current_format")
                      or "steel_quality_v1")
        
        # 通过工厂获取引擎实例（惰性单例）
        engine = get_engine(engine_name)
        
        # 执行OCR识别
        text_lines = engine.recognize(image_input)
        
        # 检查OCR结果
        if not text_lines:
            return "OCR未识别到任何文本"
        
        # 通过工厂获取格式处理器并处理结果
        processor = get_format(format_name)
        result = processor.process(text_lines)
        
        processing_time = time.time() - start_time
        return result
        
    except Exception as e:
        return f"处理失败: {str(e)}"
