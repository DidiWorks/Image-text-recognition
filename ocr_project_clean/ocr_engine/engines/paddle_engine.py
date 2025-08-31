"""
PaddleOCR引擎实现
"""
try:
    import numpy as np
except ImportError:
    np = None

try:
    from paddleocr import PaddleOCR
except ImportError:
    PaddleOCR = None

class PaddleOCREngine:
    """PaddleOCR引擎"""
    
    def __init__(self):
        if PaddleOCR is None:
            raise ImportError("PaddleOCR未安装，请运行: pip install paddleocr")
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    
    def recognize(self, image):
        """识别图片文字"""
        if np is None:
            raise ImportError("numpy未安装，请运行: pip install numpy")
        img_np = np.array(image)
        results = self.ocr.ocr(img_np)
        
        if not results or not results[0]:
            return []
        
        # 处理OCR结果
        blocks = []
        for line in results[0]:
            if line and len(line) >= 2:
                box = line[0]
                text = line[1][0]
                x = np.mean([point[0] for point in box])
                y = np.mean([point[1] for point in box])
                blocks.append({'text': text, 'x': x, 'y': y})
        
        # 按坐标重组文本行
        return self._reorganize_lines(blocks)
    
    def _reorganize_lines(self, blocks):
        """重组文本行"""
        # 按y排序，分行
        blocks.sort(key=lambda b: b['y'])
        lines = []
        current_line = []
        last_y = None
        y_threshold = 10
        
        for b in blocks:
            if last_y is None or abs(b['y'] - last_y) < y_threshold:
                current_line.append(b)
            else:
                lines.append(current_line)
                current_line = [b]
            last_y = b['y']
        
        if current_line:
            lines.append(current_line)
        
        # 每行内容直接拼接
        text_lines = []
        for line in lines:
            line_sorted = sorted(line, key=lambda b: b['x'])
            line_text = ''.join([b['text'] for b in line_sorted])
            text_lines.append(line_text)
        
        return text_lines
    
    def get_engine_name(self):
        return "PaddleOCR"
