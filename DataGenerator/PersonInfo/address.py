import string

from faker import Faker
import random
import re

fake = Faker("zh_CN")

def generate_home_addresses(n: int) -> list[str]:
    """
    批量生成家庭地址

    Args:
        n (int): 生成的数量

    Returns:
        list[str]: 生成的家庭住址列表
    """

    return [_generate_custom_address() for _ in range(n)]

# 移除邮编（末尾的六位数字）
def _clean_faker_address(raw_address: str) -> str:
    return re.sub(r'\s*\d{6}$', '', raw_address)

# 随机生成楼栋号
def _random_building_suffix():
    formats = [
        "{letter}座",
        "{num}号楼",
        "{num}单元",
        "{num}栋"
    ]
    fmt = random.choice(formats)

    # 随机生成字母（A~Z）或数字（1~50）
    letter = random.choice(string.ascii_uppercase)
    num = random.randint(1, 50)

    return fmt.format(letter=letter, num=num)

# 拼接地址
def _generate_custom_address() -> str:
    raw = fake.address()
    base = re.sub(r'\s*\d{6}$', '', raw)

    building = _random_building_suffix()
    door = f"{random.randint(100, 999)}号"

    return re.sub(r'[a-zA-Z]', lambda m: m.group().upper(), f"{base}{building}{door}")



