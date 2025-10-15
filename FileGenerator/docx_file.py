import os
import random
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from pathlib import Path

from DataGenerator.Content.document import *

# 输入输出目录
# 目录配置
txt_dir = "/Users/lyu/TMP/6/tmp/text_word"
# docx_dir = "/Users/lyu/TMP/6/tmp/word"
# 可选字体（请确保系统有这些字体）
fonts = ['宋体', '微软雅黑', 'Arial', 'Times New Roman', 'Calibri', '仿宋', '黑体']

# 字号选项（磅）
font_sizes = [10, 11, 12, 14, 16]

# 段落对齐方式
alignments = [
    WD_ALIGN_PARAGRAPH.LEFT,
    WD_ALIGN_PARAGRAPH.CENTER,
    WD_ALIGN_PARAGRAPH.RIGHT,
    WD_ALIGN_PARAGRAPH.JUSTIFY
]

def make_docx(content:str,docx_dir:str, filename:str):
    os.makedirs(docx_dir, exist_ok=True)
    txt_to_docx(content, docx_dir, filename)


def random_color():
    # 颜色不宜太鲜艳，控制在低亮度
    return RGBColor(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))

def set_run_font(run):
    font_name = random.choice(fonts)
    run.font.name = font_name
    run.font.size = Pt(random.choice(font_sizes))
    run.font.color.rgb = random_color()
    # 让Word正确识别中文字体
    rFonts = run._element.rPr.rFonts
    rFonts.set(qn('w:eastAsia'), font_name)

def random_paragraph_style(paragraph):
    paragraph.alignment = random.choice(alignments)
    for run in paragraph.runs:
        # 随机加粗、斜体、下划线
        run.bold = random.random() < 0.3
        run.italic = random.random() < 0.2
        run.underline = random.random() < 0.1
        set_run_font(run)

def txt_to_docx(content:str, docx_path, filename):
    document = Document()
    # 按两个换行符分段
    paragraphs = content.split("\n\n")
    for para_text in paragraphs:
        para_text = para_text.strip()
        if not para_text:
            continue
        para = document.add_paragraph(para_text)
        random_paragraph_style(para)

    document.save(Path(docx_path)/filename )



if __name__ == "__main__":
    for i in range(1688):
        make_docx(
            generate_document_content(generate_num=1)[0],
            docx_dir="/Users/lyu/Code/GitHub/PythonScripts/tmp_out",
            filename=f"{i+1}.docx"
        )