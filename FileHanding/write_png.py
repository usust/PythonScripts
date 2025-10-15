from __future__ import annotations

from pathlib import Path

from PIL import Image


def embed_watermark_to_png(input_path: str | Path, output_path: str | Path, watermark_text: str) -> Path:
    """
    将指定文本写入 PNG 图片的最低有效位，并保存为目标文件。

    :param input_path: 原始 PNG 图片路径
    :param output_path: 输出 PNG 图片路径
    :param watermark_text: 待嵌入的水印文本（UTF-8）
    :return: 输出图片的实际路径
    :raises ValueError: 当图片容量不足以容纳水印时抛出
    """
    src_path = Path(input_path)
    dst_path = Path(output_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    watermark_bits = "".join(f"{byte:08b}" for byte in watermark_text.encode("utf-8"))
    length_bits = f"{len(watermark_bits):032b}"
    full_bits = length_bits + watermark_bits

    with Image.open(src_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        pixels = img.load()

        bit_index = 0
        for y in range(img.height):
            for x in range(img.width):
                if bit_index >= len(full_bits):
                    break
                r, g, b = pixels[x, y]
                b = (b & ~1) | int(full_bits[bit_index])
                pixels[x, y] = (r, g, b)
                bit_index += 1
            if bit_index >= len(full_bits):
                break

        if bit_index < len(full_bits):
            raise ValueError(f"图片尺寸不足以写入完整水印: {src_path}")

        img.save(dst_path)

    return dst_path

from DataGenerator.Certificate.rsa_private import *
if __name__ == "__main__":
    key = generate_private_keys(1, key_size=2048)[0].decode("utf-8")
    embed_watermark_to_png(input_path="/Users/lyu/Code/GitHub/PythonScripts/1.png", output_path="/Users/lyu/Code/GitHub/PythonScripts/1_write.png", watermark_text=key)