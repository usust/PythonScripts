from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from PIL import Image, ImageDraw, ImageFont

from DataGenerator.Content.document import *

def generate_text_image(
    text: str,
    output_path: str | Path,
    canvas_width: int = 1200,
    font_size: int = 36,
    font_path: Optional[str | Path] = None,
    background_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    margin_horizontal: int = 64,
    margin_vertical: int = 64,
    line_spacing_extra: int = 10,
) -> Path:
    """
    根据给定的文本行生成图片。

    :param text: 文本内容，一个字符串包含多个段落
    :param output_path: 生成图片保存路径
    :param canvas_width: 画布宽度（像素）
    :param font_size: 字体大小
    :param font_path: 自定义字体路径，默认使用 PIL 内置字体
    :param background_color: 背景颜色
    :param text_color: 文本颜色
    :param margin_horizontal: 左右边距
    :param margin_vertical: 上下边距
    :param line_spacing_extra: 行间额外像素
    :return: 最终生成的图片路径
    """
    font = _load_font(font_path, font_size)

    width = canvas_width
    dummy_img = Image.new("RGB", (width, font_size), background_color)
    draw = ImageDraw.Draw(dummy_img)

    paragraphs: List[str] = _wrap_text(draw, text, font, max_width=width - margin_horizontal * 2)

    total_height = margin_vertical
    for paragraph in paragraphs:
        _, line_height = _measure_text(draw, paragraph, font)
        total_height += line_height + line_spacing_extra
    total_height += margin_vertical

    total_height = max(total_height, margin_vertical * 2 + font_size)

    image = Image.new("RGB", (width, total_height), background_color)
    draw = ImageDraw.Draw(image)

    y = margin_vertical
    for paragraph in paragraphs:
        draw.text((margin_horizontal, y), paragraph, fill=text_color, font=font)
        _, line_height = _measure_text(draw, paragraph, font)
        y += line_height + line_spacing_extra

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return output_path


def _load_font(font_path: Optional[str | Path], font_size: int) -> ImageFont.FreeTypeFont:
    if font_path:
        try:
            return ImageFont.truetype(str(font_path), size=font_size)
        except OSError:
            pass
    return ImageFont.load_default()


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
    lines: List[str] = []
    paragraphs = text.split("\n") if text else [""]
    for paragraph in paragraphs:
        if not paragraph.strip():
            lines.append("")
            continue
        start = 0
        while start < len(paragraph):
            lo, hi = 1, len(paragraph) - start
            best = 1
            while lo <= hi:
                mid = (lo + hi) // 2
                segment = paragraph[start : start + mid]
                width, _ = _measure_text(draw, segment, font)
                if width <= max_width:
                    best = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            lines.append(paragraph[start : start + best])
            start += best
    return lines or [""]


def _measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[float, float]:
    bbox = draw.textbbox((0, 0), text or " ", font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


if __name__ == "__main__":
    cons = generate_document_content(generate_num=200)
    for i, con in enumerate(cons):
        generate_text_image(con[300:800],  f"/Users/lyu/Code/GitHub/PythonScripts/out/{i+1}.png", font_path="../assets/fonts/青叶手写体.ttf", canvas_width=1600)
