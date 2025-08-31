# 关键词管理模块
import tkinter as tk
import json
import os
from datetime import datetime
from window_utils import center_window
from window_utils import info, warn, error, ask_yes_no
KEYWORDS_CONFIG_FILE = "config/quality_keywords.json"

def load_quality_keywords():
    """从配置文件加载质量问题关键词"""
    try:
        if os.path.exists(KEYWORDS_CONFIG_FILE):
            with open(KEYWORDS_CONFIG_FILE, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                return cfg.get("quality_keywords", [])
        else:
            default_keywords = [
                "超宽", "窄尺", "卷曲", "超厚", "超薄", "终轧",
                "缺陷", "破损", "划痕", "污渍", "变形", "开裂",
                "气泡", "凹陷", "色差", "尺寸偏差", "表面粗糙"
            ]
            save_quality_keywords(default_keywords)
            return default_keywords
    except Exception as e:
        return ["超宽", "窄尺", "卷曲", "超厚", "超薄", "终轧"]

def save_quality_keywords(keywords):
    """保存质量问题关键词到配置文件"""
    try:
        os.makedirs(os.path.dirname(KEYWORDS_CONFIG_FILE), exist_ok=True)
        cfg = {
            "quality_keywords": keywords,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
        }
        with open(KEYWORDS_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False

def show_keywords_manager(parent=None):
    """显示关键词管理窗口"""  
    kw_win = tk.Toplevel(parent) if parent else tk.Toplevel()
    if parent:
        kw_win.transient(parent)
        kw_win.grab_set()
        kw_win.lift()
        kw_win.focus_force()
    kw_win.title("质量问题关键词管理")
    kw_win.geometry("700x600")  #
    center_window(kw_win, 700, 600) #
    kw_win.resizable(True, True)

    main_frame = tk.Frame(kw_win)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    tk.Label(main_frame, text="质量问题关键词管理",
             font=("Microsoft YaHei", 16, "bold")).pack(pady=(0, 20))

    list_frame = tk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    tk.Label(list_frame, text="当前关键词列表：",
             font=("Microsoft YaHei", 12, "bold")).pack(anchor='w')

    text_frame = tk.Frame(list_frame)
    text_frame.pack(fill=tk.BOTH, expand=True)

    keywords_text = tk.Text(text_frame, height=15, width=60, font=("Microsoft YaHei", 10))
    sb = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=keywords_text.yview)
    keywords_text.configure(yscrollcommand=sb.set)
    keywords_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sb.pack(side=tk.RIGHT, fill=tk.Y)

    current_keywords = load_quality_keywords()
    keywords_text.insert('1.0', '\n'.join(current_keywords))

    add_frame = tk.Frame(main_frame)
    add_frame.pack(fill=tk.X, pady=12)
    tk.Label(add_frame, text="添加新关键词：", font=("Microsoft YaHei", 11, "bold")).pack(anchor='w')

    row = tk.Frame(add_frame)
    row.pack(fill=tk.X, pady=4)
    tk.Label(row, text="关键词:").pack(side=tk.LEFT)
    new_kw_entry = tk.Entry(row, width=25, font=("Microsoft YaHei", 10))
    new_kw_entry.pack(side=tk.LEFT, padx=8)
    
    def add_keyword():
        kw = new_kw_entry.get().strip()
        if not kw:
            warn("输入错误", "请输入关键词！", parent=kw_win)
            return
        existing = [l.strip() for l in keywords_text.get("1.0", tk.END).splitlines() if l.strip()]
        if kw in existing:
            warn("关键词已存在", f'"{kw}"已存在', parent=kw_win)
            return
        keywords_text.insert(tk.END, f"\n{kw}")
        new_kw_entry.delete(0, tk.END)
        save_quality_keywords([l.strip() for l in keywords_text.get("1.0", tk.END).splitlines() if l.strip()])
        info("添加成功", f"已添加：{kw}", parent=kw_win)
        
    tk.Button(row, text="添加关键词", command=add_keyword,
              bg="green", fg="white").pack(side=tk.LEFT, padx=8)
        
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=14)

    def save_keywords():
        all_keywords = [l.strip() for l in keywords_text.get("1.0", tk.END).splitlines() if l.strip()]
        if save_quality_keywords(all_keywords):
            info("保存成功", f"已保存 {len(all_keywords)} 个关键词", parent=kw_win)
        else:
            error("保存失败", "保存关键词配置失败！", parent=kw_win)

    def reset_keywords():
        default_keywords = [
            "超宽", "窄尺", "卷曲", "超厚", "超薄", "终轧",
            "缺陷", "破损", "划痕", "污渍", "变形", "开裂"
        ]
        keywords_text.delete("1.0", tk.END)
        keywords_text.insert("1.0", "\n".join(default_keywords))
        info("重置完成", "已重置为默认关键词", parent=kw_win)

    tk.Button(btn_frame, text="保存配置", command=save_keywords,
              bg="blue", fg="white", width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="重置默认", command=reset_keywords,
              bg="orange", fg="white", width=12).pack(side=tk.LEFT, padx=5)