import pytesseract
from PIL import Image, ImageOps
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# 字体文件路径（你的字体素材目录）
font_dir = "assets/"
fonts = {
    "name_font": os.path.join(font_dir, "hei.ttf"),         # 姓名字体
    "other_font": os.path.join(font_dir, "hei.ttf"),        # 其他字段字体
    "bdate_font": os.path.join(font_dir, "fzhei.ttf"),      # 出生日期字体
    "id_font": os.path.join(font_dir, "ocrb10bt.ttf"),      # 身份证号码字体
}

# target_idcard = "650121194512180241"
log_file = "idcard_result.log"

# 根据你身份证图片尺寸测量出的区域坐标示例（left, upper, right, lower）
regions = {
    "姓名": (100, 300, 600, 400),         # 示例坐标，需自己测量
    "出生日期": (100, 500, 700, 600),
    "身份证号码": (1000, 1300, 1900, 1400),
    # 也可以加“性别”、“民族”、“住址”等区域
}

# 覆盖身份证号码区域坐标，使其与生成图片的绘制位置对齐。
# 生成图中号码绘制约在 (x≈950, y≈1475)，这里给出略宽松的裁剪框。
regions.update({
    "身份证号码": (900, 1400, 2050, 1600)
})

def log_message(message):
    print(message)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def ocr_region(img, box, lang="chi_sim", psm=3, config_extra: str = "", preprocess: bool = False):
    """裁剪图片指定区域，使用 tesseract 识别；可选灰度增强与放大。"""
    region_img = img.crop(box)
    if preprocess:
        from PIL import ImageOps
        region_img = ImageOps.grayscale(region_img)
        region_img = ImageOps.autocontrast(region_img)
        w, h = region_img.size
        region_img = region_img.resize((int(w * 2), int(h * 2)))
    # 针对英文数字单行（身份证号码）自动启用白名单与预处理
    auto_whitelist = (lang == "eng" and psm == 7 and not config_extra)
    if auto_whitelist:
        config_extra = "-c tessedit_char_whitelist=0123456789Xx"
        preprocess = True
    config = f'--psm {psm}' + (f" {config_extra}" if config_extra else "")
    text = pytesseract.image_to_string(region_img, lang=lang, config=config)
    return text.strip().replace(" ", "").replace("\n", "")

def extract_idcard_info(image_path):
    try:
        img = Image.open(image_path)
        info = {}

        # 姓名区域识别（用中文简体）
        name_text = ocr_region(img, regions["姓名"], lang="chi_sim", psm=7)
        info["姓名"] = name_text

        # 出生日期区域识别（中文简体）
        bdate_text = ocr_region(img, regions["出生日期"], lang="chi_sim", psm=7)
        info["出生日期"] = bdate_text

        # 身份证号码区域识别（英文+数字，单行）
        id_text = ocr_region(img, regions["身份证号码"], lang="eng", psm=7)
        # 只取符合身份证号格式的字符串
        if re.fullmatch(r"\d{17}[\dXx]", id_text):
            info["身份证号码"] = id_text
        else:
            # 如果不匹配，可以做后备全图OCR和正则匹配
            full_text = pytesseract.image_to_string(img, lang="chi_sim")
            full_text_clean = full_text.replace(" ", "").replace("\n", "")
            match = re.search(r"公民身份号码(\d{17}[\dXx])", full_text_clean)
            if match:
                info["身份证号码"] = match.group(1)

        # 你可以继续加 性别、民族、住址区域识别等...

        return info

    except Exception as e:
        return {"错误": str(e)}

def process_image(img_path):
    info = extract_idcard_info(img_path)
    filename = os.path.basename(img_path)

    if not info or "身份证号码" not in info:
        return f"[跳过] {filename} 未识别到身份证号码", False

    output_lines = [f"[识别] {filename}"]
    for k, v in info.items():
        output_lines.append(f"  {k}: {v}")

    # if "身份证号码" in info and info["身份证号码"] == target_idcard:
    #     output_lines.append(f"  [匹配] 身份证号码匹配目标: {target_idcard}")
    #     return "\n".join(output_lines), True

    return "\n".join(output_lines), False

def process_idcards_multithread(folder_path, max_workers=4):
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== 身份证扫描开始 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
             if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_image, f): f for f in files}
        for future in as_completed(futures):
            try:
                result, matched = future.result()
            except Exception as e:
                result = f"[错误] 处理时异常: {e}"
                matched = False
            log_message(result)
            if matched:
                log_message(f"=== 找到目标身份证，程序退出 ===")
                executor.shutdown(wait=False)
                return

    log_message(f"=== 身份证扫描结束 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

if __name__ == "__main__":
    folder = "output"
    process_idcards_multithread(folder, max_workers=4)
