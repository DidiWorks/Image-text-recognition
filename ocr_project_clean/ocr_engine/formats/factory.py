"""
Format 工厂（最小可用版）

用途：
- 通过名字创建格式处理器实例，避免业务层直接依赖具体类。
- 目前处理器很轻量，无需单例，每次新建即可。

对外接口：
- list_formats() -> List[str]         # 给下拉菜单显示
- get_format(name: str) -> Processor  # 名称非法时回退 'steel_quality_v1'
"""

from .steel_quality import SteelQualityFormat
from .generic_text import GenericTextFormat

# 名称 -> 格式处理器类
_FORMAT_REGISTRY = {
    "steel_quality_v1": SteelQualityFormat,
    "generic_v1": GenericTextFormat,
}

def list_formats():
    """列出可用格式名称（用于下拉菜单）。"""
    return list(_FORMAT_REGISTRY.keys())

def get_format(name: str):
    """按名称获取格式实例；未知名称回退到 'steel_quality_v1'。"""
    key = (name or "steel_quality_v1").lower()
    if key not in _FORMAT_REGISTRY:
        key = "steel_quality_v1"
    return _FORMAT_REGISTRY[key]()
