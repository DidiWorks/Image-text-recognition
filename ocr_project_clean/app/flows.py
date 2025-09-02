import time
import tkinter as tk
from tkinter import filedialog, ttk

from camera_widget import CameraWindow
from cropper import select_and_crop_enhanced
from ocr_engine import ocr_image

from menu_utils import load_config
from .logger import logger, log_ocr_operation


@log_ocr_operation(logger)
def capture_and_recognize(root):
    """拍照识别流程"""
    logger.log_ocr_start("开始拍照识别流程")
    try:
        # 摄像头进度条
        progress_window = tk.Toplevel(root)
        progress_window.title("打开摄像头")
        progress_window.geometry("400x120")
        progress_window.resizable(False, False)
        progress_window.transient(root)
        progress_window.grab_set()

        # 居中
        progress_window.update_idletasks()
        sw, sh = progress_window.winfo_screenwidth(), progress_window.winfo_screenheight()
        x, y = (sw - 400) // 2, (sh - 120) // 2
        progress_window.geometry(f"400x120+{x}+{y}")

        # 进度条
        progress = ttk.Progressbar(progress_window, maximum=100, length=350)
        progress.pack(pady=15)
        label = tk.Label(progress_window, text="正在打开摄像头...")
        label.pack()

        try:
            for i in range(1, 81, 2):
                progress["value"] = i
                if i < 30:
                    label.config(text="正在检测摄像头设备...")
                elif i < 60:
                    label.config(text="正在初始化摄像头...")
                else:
                    label.config(text="正在连接摄像头...")
                progress_window.update()
                time.sleep(0.01)

            label.config(text="摄像头连接中...")
            progress_window.update()

            camera_win = CameraWindow(root, save_dir='captured')

            for i in range(80, 101, 5):
                progress["value"] = i
                label.config(text="摄像头已就绪")
                progress_window.update()
                time.sleep(0.01)

        finally:
            progress_window.destroy()

        root.wait_window(camera_win)
        img_path = camera_win.image_path

        if img_path:
            logger.log_ocr_result("拍照", f"拍照成功: {img_path}", 1.0, 0.0)

            cropped_img = select_and_crop_enhanced(img_path)
            if cropped_img:
                _ocr_then_export_and_compare(root, cropped_img)
            else:
                logger.log_ocr_error("截图选择", "用户取消截图")
        else:
            logger.log_ocr_error("拍照", "拍照失败或用户取消")
    except Exception as e:
        logger.log_ocr_error("拍照识别", f"发生错误: {str(e)}")


@log_ocr_operation(logger)
def select_and_recognize(root):
    """选择图片识别流程"""
    logger.log_ocr_start("开始选择图片识别流程")
    try:
        img_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg;*.png;*.bmp')], parent=root)
        if img_path:
            logger.log_ocr_result("选择图片", f"选择图片: {img_path}", 1.0, 0.0)

            cropped_img = select_and_crop_enhanced(img_path)
            if cropped_img:
                _ocr_then_export_and_compare(root, cropped_img)
            else:
                logger.log_ocr_error("截图选择", "用户取消截图")
        else:
            logger.log_ocr_error("选择图片", "用户取消选择图片")
    except Exception as e:
        logger.log_ocr_error("选择图片识别", f"发生错误: {str(e)}")


def _ocr_then_export_and_compare(root, cropped_img):
    """OCR -> 导出 -> 对比窗口"""
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()

    # OCR进度条
    ocr_window = tk.Toplevel(root)
    ocr_window.title("OCR识别中")
    ocr_window.geometry("400x120")
    ocr_window.resizable(False, False)
    ocr_window.transient(root)
    ocr_window.grab_set()

    ocr_window.update_idletasks()
    x, y = (sw - 400) // 2, (sh - 120) // 2
    ocr_window.geometry(f"400x120+{x}+{y}")

    ocr_progress = ttk.Progressbar(ocr_window, maximum=100, length=350)
    ocr_progress.pack(pady=15)
    ocr_label = tk.Label(ocr_window, text="正在加载OCR引擎...")
    ocr_label.pack()

    try:
        for i in range(1, 71, 2):
            ocr_progress["value"] = i
            if i < 20:
                ocr_label.config(text="正在加载OCR引擎...")
            elif i < 40:
                ocr_label.config(text="正在初始化识别模型...")
            elif i < 60:
                ocr_label.config(text="正在预处理图像...")
            else:
                ocr_label.config(text="正在准备识别...")
            ocr_window.update()
            time.sleep(0.01)

        ocr_label.config(text="正在识别文字...")
        ocr_window.update()

        start_time = time.time()
        text = ocr_image(cropped_img)
        processing_time = time.time() - start_time

        for i in range(70, 101, 5):
            ocr_progress["value"] = i
            ocr_label.config(text="识别完成")
            ocr_window.update()
            time.sleep(0.01)

    finally:
        ocr_window.destroy()

    logger.log_ocr_result("OCR识别", text, 0.9, processing_time)



    # 对比窗口
    from gui_utils import show_compare_window
    show_compare_window(root, cropped_img, text)


