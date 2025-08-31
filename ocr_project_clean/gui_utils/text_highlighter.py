"""
文本高亮模块
"""
import tkinter as tk
from .keywords_manager import load_quality_keywords

def apply_highlighting(text_widget):
    """应用关键词高亮"""
    try:
        # 配置高亮标签
        text_widget.tag_configure("quality_issue", background="yellow", foreground="red")
        
        # 获取文本内容和关键词
        text_content = text_widget.get("1.0", tk.END)
        keywords = load_quality_keywords()
        
        # 为每个关键词添加高亮
        for keyword in keywords:
            if keyword in text_content:
                # 找到所有关键词位置并高亮
                start_pos = "1.0"
                while True:
                    pos = text_widget.search(keyword, start_pos, tk.END)
                    if not pos:
                        break
                    end_pos = f"{pos}+{len(keyword)}c"
                    text_widget.tag_add("quality_issue", pos, end_pos)
                    start_pos = end_pos
                    
    except Exception as e:
        pass

def refresh_highlighting(text_widget):
    """刷新高亮"""
    try:
        # 清除所有现有标签（保留选择标签）
        for tag in text_widget.tag_names():
            if tag != "sel":
                text_widget.tag_remove(tag, "1.0", tk.END)
        
        # 重新应用高亮
        apply_highlighting(text_widget)
    except Exception as e:
        pass
