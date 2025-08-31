import tkinter as tk
from window_utils import center_window
from menu_utils import create_menu_bar
from .flows import capture_and_recognize, select_and_recognize
from .logger import logger, on_exit


def run_app():
    root = tk.Tk()
    root.title("OCR自动识别工具 v1.0")
    root.geometry("300x200")
    center_window(root, 300, 200)

    # 启动日志
    logger.log_ocr_start("程序启动")

    # 菜单
    create_menu_bar(root, lambda: select_and_recognize(root))

    # 主界面
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill=tk.BOTH)

    btn_capture = tk.Button(frame, text="拍照识别", command=lambda: capture_and_recognize(root))
    btn_capture.pack(pady=10, fill=tk.X)

    btn_select = tk.Button(frame, text="选择图片识别", command=lambda: select_and_recognize(root))
    btn_select.pack(pady=10, fill=tk.X)

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))
    root.mainloop()


