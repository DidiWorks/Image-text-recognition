"""
通用文本格式
"""

class GenericTextFormat:
    """通用文本格式"""
    
    def __init__(self, wrap_width=30):
        self.wrap_width = wrap_width
    
    def process(self, text_lines):
        """处理通用文本格式"""
        # 简单换行处理
        wrapped_lines = []
        for line in text_lines:
            if len(line) <= self.wrap_width:
                wrapped_lines.append(line)
            else:
                # 按宽度换行
                for i in range(0, len(line), self.wrap_width):
                    wrapped_lines.append(line[i:i+self.wrap_width])
        
        result = "\n".join(wrapped_lines)
        return result
    
    def get_format_name(self):
        return "generic_v1"
