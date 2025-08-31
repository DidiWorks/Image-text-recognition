"""
图片处理工具
"""
try:
    import cv2
except ImportError:
    cv2 = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    from PIL import Image
except ImportError:
    Image = None

def check_image(img):
    """检查图片是否有效"""
    if img is None:
        return False
    
    # 转换为numpy数组
    if isinstance(img, str):
        # 如果是文件路径
        if cv2 is not None:
            img = cv2.imread(img)
        else:
            return True  # 假设图片有效
    
    if img is None:
        return False
    
    # 检查图片尺寸
    if hasattr(img, 'shape'):
        height, width = img.shape[:2]
        
        if width < 10 or height < 10:
            return False
    
    return True

def convert_image(img):
    """转换图片格式"""
    if isinstance(img, str):
        # 如果是文件路径，加载图片
        if Image is not None:
            img = Image.open(img)
        else:
            return img
    
    # 转换为numpy数组
    if hasattr(img, 'save'):  # PIL Image
        if np is not None:
            img_np = np.array(img)
        else:
            return img
    else:
        img_np = img
    
    return img_np
