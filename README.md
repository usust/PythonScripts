# PythonScriptProject

常用的Python脚本合集，主要包含了数据生成模块。

## 运行方式

在项目的根目录下执行，以模块的形式执行。例如：

```bash
    python3 -m FileGenerator.id_picture.chinese_id_picture
```

## 安装依赖

本项目已提供 `pyproject.toml`，建议使用可选依赖进行按需安装：

```bash
python3 -m pip install -e .           # 基础依赖
python3 -m pip install -e '.[image]'  # 图像相关：numpy/opencv/Pillow
python3 -m pip install -e '.[docx]'   # docx 相关：python-docx
python3 -m pip install -e '.[pcap]'   # pcap 相关：scapy
python3 -m pip install -e '.[crypto]' # 加密相关：cryptography
python3 -m pip install -e '.[ocr]'    # OCR 相关：pytesseract
python3 -m pip install -e '.[all]'    # 全部依赖
```

说明：
- `pytesseract` 仅是 Python 封装，还需要系统里安装 `tesseract` 可执行文件。
- 如果只使用部分功能，建议安装对应的可选依赖组。

## DataGenerator

### 证书信息

- rsa 私钥信息：生成单条RSA私钥信息。

### 内容生成

- 文档内容：根据模版生成一个填充文档的文本内容，支持指定内容的长度。
- 段落/句子：根据模版生成一段话，支持指定长度。
- 随机字符串：生成一个长度不超过 max_length 的随机字符串，可通过 `min_length` 限制最短字符串长度。

### 时间日期

- 日期：在指定范围内随机生成日期字符串。

### 数值

- 支持生成浮点数和整数。
- 生成长度为 n 的布尔序列，可指定 True 大致占据指定比例。

### 个人信息

- 支持生成邮箱地址、手机号、中文姓名、银行卡号、国际移动设备识别码(IMEI)、职业、地址位置（粗略）。

## 文件生成

### 流量包pcap

生成ssh流量包、支持随机生成定量的干扰流量包自定义组合。

- ssh流量包：支持传输文件

### 身份证图片生成

支持批量生成身份证图片，只生成正面图片，同时支持 OCR 识别生成的身份证图片。

### 常规文件

支持生成csv、docx、email、rsa私钥证书、（文本）图片的生成。


## 文件处理
- png图片插入到docx文件中
- 重置文件创建时间信息
- 随机重命名文件：可指定长度
- png图片隐写
