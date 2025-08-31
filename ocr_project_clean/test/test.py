# generate_test_image.py
from PIL import Image, ImageDraw, ImageFont
import os, random

W, H = 1600, 600
BG = (255, 255, 255)
FG = (20, 20, 20)
LINE_HEIGHT = 44
LEFTS = [40, 360, 600, 900, 1200]  # 多列X起点（可按需改）
ROWS = [
    # 卷号,         坯号,        牌号,    备注1,           备注2
    ("A1234567890", "9999999999", "ASDD1", "长尾：尾6米内", "文字质量问题"),
    ("B2345678901", "1234567890", "Q235B", "表面划伤",       "需复检"),
    ("C3456789012", "A123456789", "SPHC",  "卷尾开裂",       "边部破损"),
    ("D4567890123", "8888888888", "HC340", "错字/粘连",      "检查设备"),
]

def get_font(size=28):
    # 优先使用常见中文字体；找不到就用默认
    for name in ["msyh.ttc", "simhei.ttf", "simkai.ttf", "simfang.ttf", "simsun.ttc"]:
        p = os.path.join("C:\\Windows\\Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_row(draw, y, cols, font):
    # 模拟轻微排版抖动（更贴近OCR真实输出）
    for i, text in enumerate(cols):
        x = LEFTS[i] + random.randint(-2, 2)
        yy = y + random.randint(-2, 2)
        draw.text((x, yy), text, fill=FG, font=font)

def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    title_font = get_font(30)
    font = get_font(28)

    # 标题
    draw.text((40, 20), "钢材质量样表（测试用）", fill=(0, 0, 180), font=title_font)

    # 表头
    headers = ("卷号", "坯号", "牌号", "说明", "备注")
    draw_row(draw, 80, headers, font)
    draw.line([(30, 115), (W-30, 115)], fill=(200, 200, 200), width=2)

    # 内容
    y = 130
    for row in ROWS:
        draw_row(draw, y, row, font)
        y += LINE_HEIGHT

    # 额外一行：只给“坯号/牌号”，缺少卷号，测试可缺字段解析
    partial = ("", "7777777777", "ASD+Z10", "位数不固定", "仅测试缺卷号")
    draw_row(draw, y, partial, font)

    os.makedirs("output", exist_ok=True)
    out_path = os.path.join("output", "steel_quality_test.png")
    img.save(out_path)
    print("saved:", out_path)

if __name__ == "__main__":
    main()