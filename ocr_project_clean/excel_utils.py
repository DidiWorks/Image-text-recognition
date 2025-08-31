# 原来excel 输出模块 待优化
# excel_utils.py
import openpyxl
import os
from datetime import datetime

def save_to_excel(text, output_path="output/output_keywords.xlsx"):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if os.path.exists(output_path):
            wb = openpyxl.load_workbook(output_path)
            ws = wb.active
        else:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "OCR识别结果"
            ws.append(["识别文本", "识别时间"])  # 表头

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append([str(text), current_time])     # 末尾追加一行
        wb.save(output_path)
        return True
    except Exception as e:
        return False