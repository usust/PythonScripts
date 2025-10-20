# coding:utf-8
# from: https://github.com/airob0t/idcardgenerator

import os
import sys
import csv
import numpy as np
import cv2
from PIL import Image as PImage, ImageFont, ImageDraw
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from DataGenerator.PersonInfo.name import *
from DataGenerator.PersonInfo.id_card import *
from DataGenerator.PersonInfo.address import *
from DataGenerator.PersonInfo.nation import *

# 获取 base_dir
if getattr(sys, 'frozen', None):
    assets_dir = os.path.join(sys._MEIPASS, 'assets')
else:
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')


def create_person_csv(person_count:int, csv_path:str)->list[dict[str,str]]:
    """
    生成指定数量的人员信息 CSV 文件，并返回相同的数据列表。

    参数:
    - person_count: 需要生成的人员数量。
    - csv_path: 输出 CSV 文件路径（若父目录不存在会自动创建）。

    返回:
    - rows: 人员信息列表 list[dict[str,str]]，每个元素包含：
      avatar_path, name, sex, nation, year, mon, day, addr, idn, auto_cut_bg。

    说明:
    - 函数会将生成的数据写入 csv_path 指定的 CSV，并同时返回内存中的相同数据，便于后续直接使用。
    """
    headers = [
        "avatar_path", "name", "sex", "nation",
        "year", "mon", "day", "addr", "idn","auto_cut_bg"
    ]
    
    out_dir = Path(csv_path).parent
    if str(out_dir) != "" and not out_dir.exists():
        os.makedirs(out_dir, exist_ok=True)

    # 收集并返回生成的用户信息，同时写入 CSV
    rows = []
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        names = generate_unique_names(person_count)
        ids = generate_unique_id_numbers(person_count)
        addresses = generate_home_addresses(person_count)
        nations = generate_ethnic_sample(person_count)

        for i in range(person_count):
            y, m, d = parse_birth_ymd_from_id(ids[i])
            sex = '男' if ids[i][-2].isdigit() and int(ids[i][-2]) % 2 == 1 else '女'

            row = {
                "avatar_path": _get_random_avatar_path(),
                "name":  names[i],
                "sex": sex,
                "nation":  nations[i],
                "year": y,
                "mon": m,
                "day": d,
                "addr": addresses[i],
                "idn": ids[i],
                "auto_cut_bg": str(False)
            }
            writer.writerow(row)
            rows.append(row)
    return rows


def generate_idcard(person:dict[str,str], out_dir:Path= Path("output")):
    """
    根据给定的人员信息，生成身份证样式的图片并保存到本地。

    参数:
    - person: 人员信息字典，需包含以下键：
      avatar_path, name, sex, nation, year, mon, day, addr, idn, auto_cut_bg。

    行为/副作用:
    - 加载模板图与头像，渲染文字后保存 PNG 文件至当前工作目录，文件名形如：
      color_{name}.png。

    说明:
    - 依赖路径 `base_dir` 下的资源文件（模板/字体）。
    - 当 `auto_cut_bg` 为 True 时，尝试进行背景抠图；否则直接粘贴头像。
    - 函数无返回值，仅产生输出文件。
    """

    # 确认输出目录存在
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    im = PImage.open(os.path.join(assets_dir, 'empty.png'))
    avatar = PImage.open(person["avatar_path"])

    name_font = ImageFont.truetype(os.path.join(assets_dir, 'hei.ttf'), 72)
    other_font = ImageFont.truetype(os.path.join(assets_dir, 'hei.ttf'), 60)
    bdate_font = ImageFont.truetype(os.path.join(assets_dir, 'fzhei.ttf'), 60)  # 出生日期字体（用于年/月/日）
    id_font = ImageFont.truetype(os.path.join(assets_dir, 'ocrb10bt.ttf'), 72)

    draw = ImageDraw.Draw(im)
    draw.text((630, 690), person["name"], fill=(0, 0, 0), font=name_font)
    draw.text((630, 840), person["sex"], fill=(0, 0, 0), font=other_font)
    draw.text((1030, 840), person["nation"], fill=(0, 0, 0), font=other_font)
    draw.text((630, 980), str(person["year"]), fill=(0, 0, 0), font=bdate_font)
    draw.text((950, 980), str(person["mon"]), fill=(0, 0, 0), font=bdate_font)
    draw.text((1150, 980), str(person["day"]), fill=(0, 0, 0), font=bdate_font)

    start = 0
    loc = 1120
    addr = person["addr"]
    while start + 11 < len(addr):
        draw.text((630, loc), addr[start:start + 11], fill=(0, 0, 0), font=other_font)
        start += 11
        loc += 100
    draw.text((630, loc), addr[start:], fill=(0, 0, 0), font=other_font)
    draw.text((950, 1475), person["idn"], fill=(0, 0, 0), font=id_font)
    if person["auto_cut_bg"]:
        avatar_cv = cv2.cvtColor(np.asarray(avatar), cv2.COLOR_RGBA2BGRA)
        im_cv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGBA2BGRA)
        im_cv = _change_background(avatar_cv, im_cv, (500, 670), (690, 1500))
        im = PImage.fromarray(cv2.cvtColor(im_cv, cv2.COLOR_BGRA2RGBA))
    else:
        avatar = avatar.resize((500, 670)).convert('RGBA')
        im.paste(avatar, (1500, 690), mask=avatar)

    filename = out_dir/f"{person['name']}.png"
    im.save(filename)
    print(f"生成身份证图片 {filename} 完成")


def load_person_csv(csv_path:Path)->list[dict[str,Any]]:
    """
    从指定 CSV 中读取人员信息，并将每一行转换为字典后组成列表返回。

    参数:
    - csv_path: CSV 文件路径。

    返回:
    - list[dict[str, Any]]: 读取到的人员信息列表，其中 `auto_cut_bg` 字段会被转换为布尔值。
    """
    csv_path = Path(csv_path)
    persons: list[dict[str, Any]] = []
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV 文件不存在: {csv_path}")

    def _normalize_auto_cut(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        return str(value).strip().lower() in {"1", "true", "yes", "y", "t"}

    with open(csv_path, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            normalized = dict(row)
            normalized["auto_cut_bg"] = _normalize_auto_cut(normalized.get("auto_cut_bg"))
            persons.append(normalized)
    return persons

def _change_background(img, img_back, zoom_size, center):
    """
    将前景头像图按给定尺寸缩放，并在蓝色背景抠图的基础上粘贴到目标底图。

    参数:
    - img: 前景头像的 BGR 图像数组（OpenCV 格式）。
    - img_back: 目标底图的 BGR 图像数组，粘贴后的输出在此图上。
    - zoom_size: 元组 (w, h)，将头像缩放到的尺寸。
    - center: 元组 (y, x)，头像左上角在底图上的粘贴起始位置（行、列偏移）。

    返回:
    - 处理后的底图图像数组（BGR）。

    说明:
    - 通过 HSV 颜色空间阈值估计蓝色区域，进行腐蚀/膨胀后得到前景掩膜，
      仅在非蓝色区域将前景像素拷贝到底图，实现“蓝底证件照抠图”的效果。
    """
    img = cv2.resize(img, zoom_size)
    rows, cols, _ = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gb = hsv[0, 0]
    diff = [5, 30, 30]
    lower_blue = np.array(gb - diff)
    upper_blue = np.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    dilate = cv2.dilate(cv2.erode(mask, None, iterations=1), None, iterations=1)

    # 遍历每个像素：当掩膜值为0（非蓝色背景区域）时，
    # 将前景图对应像素拷贝到目标底图，以 center 为偏移定位粘贴位置。
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:
                img_back[center[0] + i, center[1] + j] = img[i, j]
    return img_back



def _get_random_avatar_path(avatar_dir: str = "assets/avatar") -> str:
    """
    从头像资源目录中随机选择一张图片并返回其路径。

    参数:
    - avatar_dir: 头像资源目录路径，默认使用项目内的 assets/avatar。

    返回:
    - 若目录存在且包含支持的图片文件，返回其中一张图片的完整路径；
      否则返回空字符串。

    说明:
    - 支持的图片扩展名: .png, .jpg, .jpeg, .bmp, .gif, .webp。
    """
    p = Path(avatar_dir)
    if not p.exists() or not p.is_dir():
        return ""

    exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}
    files = [str(f) for f in p.iterdir() if f.is_file() and f.suffix.lower() in exts]
    if not files:
        return ""
    return random.choice(files)



if __name__ == '__main__':
    # load from person.csv
    persons = load_person_csv(Path("person.csv"))
    # or create a random person.csv
    # persons = create_person_csv(20, "person.csv")
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(generate_idcard, persons)
