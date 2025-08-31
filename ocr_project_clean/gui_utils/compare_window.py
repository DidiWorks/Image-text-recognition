# 对比窗口模块
from window_utils import info, warn, error, ask_yes_no
import tkinter as tk
from tkinter import font, filedialog
from PIL import Image, ImageTk
from window_utils import center_window

from .keywords_manager import show_keywords_manager
from .text_highlighter import apply_highlighting, refresh_highlighting

def show_compare_window(parent, image_input, text):
    """显示对比窗口"""
    win = tk.Toplevel(parent)
    win.transient(parent)
    # win.grab_set()
    win.lift()
    win.focus_force()
    win.title('图片与识别结果对比')
    
    win.minsize(900, 600)
    center_window(win, 900, 600)
    win.resizable(True, True)

    paned = tk.PanedWindow(win, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
    paned.pack(fill=tk.BOTH, expand=True)

    # 左侧：图片
    image_frame = tk.Frame(paned, width=450, height=450, bg='gray')
    paned.add(image_frame, minsize=260)

    canvas = tk.Canvas(image_frame, bg='gray')
    hbar = tk.Scrollbar(image_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    vbar = tk.Scrollbar(image_frame, orient=tk.VERTICAL, command=canvas.yview)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    if hasattr(image_input, 'save'):
        original_img = image_input
    else:
        original_img = Image.open(image_input)
    
    img_w, img_h = original_img.size
    
    scale = [1.0]
    photo = ImageTk.PhotoImage(original_img)
    img_id = canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.config(scrollregion=(0, 0, img_w, img_h))
    canvas.image = photo

    drag = {"x": 0, "y": 0, "sx": 0, "sy": 0}
    

    def redraw():
        new_size = (int(img_w * scale[0]), int(img_h * scale[0]))
        img_resized = original_img.resize(new_size, Image.Resampling.LANCZOS)
        new_photo = ImageTk.PhotoImage(img_resized)
        canvas.itemconfig(img_id, image=new_photo)
        canvas.config(scrollregion=(0, 0, new_size[0], new_size[1]))
        canvas.image = new_photo

    def on_img_wheel(e):
        if e.state & 0x0004:  # Ctrl
            scale[0] = max(0.2, min(5.0, scale[0] * (1.1 if e.delta > 0 else 1/1.1)))
            redraw()
            return "break"
        else:
            canvas.yview_scroll(-1 * int(e.delta/120), "units")
            return "break"

    def on_img_press(e):
        drag["x"], drag["y"] = e.x, e.y
        drag["sx"], drag["sy"] = canvas.xview()[0], canvas.yview()[0]

    def on_img_drag(e):
        dx, dy = e.x - drag["x"], e.y - drag["y"]
        x_move = -dx / max(1, canvas.winfo_width())
        y_move = -dy / max(1, canvas.winfo_height())
        canvas.xview_moveto(drag["sx"] + x_move)
        canvas.yview_moveto(drag["sy"] + y_move)

    canvas.bind("<MouseWheel>", on_img_wheel)
    canvas.bind("<ButtonPress-1>", on_img_press)
    canvas.bind("<B1-Motion>", on_img_drag)

    # 右侧：文本
    text_frame = tk.Frame(paned, width=450, height=450)
    paned.add(text_frame, minsize=260)

    text_font_size = [12]
    text_font = font.Font(family="Microsoft YaHei", size=text_font_size[0])

    outer = tk.Frame(text_frame)
    outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    text_box = tk.Text(
        outer, width=60, height=24, font=text_font, wrap=tk.NONE,
        borderwidth=2, relief=tk.SUNKEN, state=tk.NORMAL, undo=True
    )
    text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    sbx = tk.Scrollbar(outer, orient=tk.HORIZONTAL, command=text_box.xview)
    sbx.pack(side=tk.BOTTOM, fill=tk.X)
    text_box['xscrollcommand'] = sbx.set

    sby = tk.Scrollbar(text_frame, command=text_box.yview)
    sby.pack(side=tk.RIGHT, fill=tk.Y)
    text_box['yscrollcommand'] = sby.set

    def on_txt_wheel(e):
        if e.state & 0x0004:  # Ctrl
            text_font_size[0] = max(8, min(32, text_font_size[0] + (1 if e.delta > 0 else -1)))
            text_font.configure(size=text_font_size[0])
            return "break"
    text_box.bind("<MouseWheel>", on_txt_wheel)

    # 绑定撤销/重做快捷键（隐藏按钮，仅保留功能）
    def _do_undo(e=None):
        try:
            text_box.edit_undo()
        except tk.TclError:
            pass
        return "break"

    def _do_redo(e=None):
        try:
            text_box.edit_redo()
        except tk.TclError:
            pass
        return "break"

    # Windows/Linux
    text_box.bind("<Control-z>", _do_undo)
    text_box.bind("<Control-y>", _do_redo)
    text_box.bind("<Control-Shift-Z>", _do_redo)
    # macOS（可选）
    text_box.bind("<Command-z>", _do_undo)
    text_box.bind("<Command-Shift-Z>", _do_redo)

    # 插入文本并应用高亮
    processed_text = text  # 直接使用原文本
    text_box.insert("1.0", processed_text)
    apply_highlighting(text_box)  # 应用自动高亮
    
    # 按钮区
    btn_bar = tk.Frame(win)
    btn_bar.pack(fill=tk.X, padx=10, pady=6)

    def copy_text():
        """复制文本到剪贴板"""
        win.clipboard_clear()
        win.clipboard_append(text_box.get("1.0", tk.END))
        # btn_copy.config(text="已复制！")
        # win.after(1200, lambda: btn_copy.config(text="复制文本"))

    def save_text():
        """保存文本到文件"""
        try:
            fname = filedialog.asksaveasfilename(
                defaultextension="txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                parent=win
            )
            if fname:
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(text_box.get("1.0", tk.END))
                info("保存成功", f"已保存到：{fname}", parent=win)
        except Exception as e:
            error("保存失败", str(e), parent=win)

    # 创建按钮
    # btn_copy = tk.Button(btn_bar, text="复制文本", command=copy_text, width=10)
    btn_save = tk.Button(btn_bar, text="保存文件", command=save_text, width=10)
    btn_high = tk.Button(btn_bar, text="刷新高亮", command=lambda: refresh_highlighting(text_box), width=10)
    btn_kw = tk.Button(btn_bar, text="管理关键词", command=lambda: show_keywords_manager(parent=win), width=10)
    btn_close = tk.Button(btn_bar, text="关闭窗口", command=win.destroy, width=10)

    # btn_copy.pack(side=tk.LEFT, padx=3)
    btn_save.pack(side=tk.LEFT, padx=3)
    btn_high.pack(side=tk.LEFT, padx=12)
    btn_kw.pack(side=tk.LEFT, padx=3)
    btn_close.pack(side=tk.RIGHT, padx=3)

    # 状态栏
    status = tk.Frame(win)
    status.pack(fill=tk.X, padx=10)
    tk.Label(status, text="说明：Ctrl+滚轮调字体，编辑后自动刷新高亮",
             anchor='w').pack(side=tk.LEFT)

    # 居中显示
    win.update_idletasks()
    ww, wh = win.winfo_width(), win.winfo_height()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - ww) // 2, (sh - wh) // 2
    win.geometry(f"{ww}x{wh}+{x}+{y}")
    
    win.wait_window()