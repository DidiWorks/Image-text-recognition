"""
Engine 工厂（最小可用版）

用途：
- 通过名字获取引擎实例，避免业务里写死具体类。
- 惰性单例：同一引擎只初始化一次（模型大，重复初始化很慢）。

对外接口：
- list_engines() -> List[str]        # 给下拉菜单显示
- get_engine(name: str) -> Engine    # 名称非法时回退 'paddle'
"""

from .paddle_engine import PaddleOCREngine

# 名称 -> 引擎类
_ENGINE_REGISTRY = {
    "paddle": PaddleOCREngine,
}

# 名称 -> 引擎实例（单例缓存）
_engine_singletons = {}

def list_engines():
    """列出可用引擎名称（用于下拉菜单）。"""
    return list(_ENGINE_REGISTRY.keys())

def get_engine(name: str):
    """按名称获取引擎实例；未知名称回退到 'paddle'；采用惰性单例。"""
    key = (name or "paddle").lower()
    if key not in _ENGINE_REGISTRY:
        key = "paddle"
    if key not in _engine_singletons:
        _engine_singletons[key] = _ENGINE_REGISTRY[key]()
    return _engine_singletons[key]