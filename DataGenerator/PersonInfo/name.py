from faker import Faker
from faker.exceptions import UniquenessException
import random
from faker import Faker

def generate_unique_names(n: int) -> list[str]:
    """
    批量生成不重复中文姓名

    Args:
        n: int, 生成的数量

    Returns:
        list[str]: 不重复姓名的列表
    """


    fake = Faker("zh_CN")
    unique_names = set()

    # 扩展用字（常见+部分生僻）
    extra_chars = [
        "景", "琪", "桐", "昊", "霖", "涵", "煜", "珺", "澜", "骁",
        "钰", "瑜", "瑶", "璇", "沐", "宸", "萱", "晟", "鑫", "铎",
        "灏", "尧", "祺", "瑾", "竣", "璟", "颢", "珂", "泓", "煦"
    ]

    # 先用 Faker 生成一部分（名字质量高）
    while len(unique_names) < min(n, 200000):  # Faker 的组合有限，先占一部分
        unique_names.add(fake.name())

    # 如果数量不足，自己组合姓氏 + 名字
    last_names = list(set(fake.last_name() for _ in range(200)))  # 常见姓氏池
    first_names = list(set(fake.first_name() for _ in range(500))) + extra_chars  # 常见名字 + 扩展字

    while len(unique_names) < n:
        last = random.choice(last_names)
        first = random.choice(first_names)
        # 30% 概率加第二个字
        if random.random() < 0.3:
            first += random.choice(first_names)
        unique_names.add(last + first)

    return list(unique_names)


