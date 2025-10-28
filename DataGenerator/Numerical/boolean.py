import random
from typing import List


def generate_boolean_sequence(
    n: int,
    true_ratio: float,
    *,
    shuffle: bool = True,
) -> List[bool]:
    """
    生成长度为 n 的布尔序列，其中 True 大致占据指定比例。

    参数:
        n: 序列长度，必须为正整数。
        true_ratio: True 值的占比，范围 [0.0, 1.0]。
    关键字参数:
        shuffle: 是否打乱 True/False 的位置，默认打乱。

    返回:
        包含 n 个布尔值的列表。

    异常:
        ValueError: 当 n 不大于 0 或 true_ratio 不在合法范围内时抛出。
    """
    if n <= 0:
        raise ValueError("n 必须为正整数")
    if not 0.0 <= true_ratio <= 1.0:
        raise ValueError("true_ratio 必须在 [0.0, 1.0] 之间")

    true_count = int(round(n * true_ratio))
    true_count = min(max(true_count, 0), n)
    false_count = n - true_count

    sequence = [True] * true_count + [False] * false_count

    if shuffle and n > 1:
        random.shuffle(sequence)

    return sequence
