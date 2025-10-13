import random
from typing import List


def generate_random_integers(n: int, lower: int, upper: int) -> List[int]:
    """
    返回包含 n 个随机整数的列表，整数范围在 [lower, upper]（含端点）。

    :param n: 需要生成的随机整数数量
    :param lower: 随机整数的下限
    :param upper: 随机整数的上限
    :return: 随机整数列表
    :raises ValueError: 当 n <= 0 或 lower > upper 时抛出
    """
    if n <= 0:
        raise ValueError("n 必须为正整数")
    if lower > upper:
        raise ValueError("lower 不能大于 upper")
    return [random.randint(lower, upper) for _ in range(n)]
