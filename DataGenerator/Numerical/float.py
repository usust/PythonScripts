import random
from typing import List


def generate_random_floats(n: int, lower: float, upper: float, decimals: int) -> List[float]:
    """
    返回包含 n 个随机浮点数的列表，浮点数范围在 [lower, upper]（含端点），并控制小数位数。

    :param n: 需要生成的随机浮点数数量
    :param lower: 随机浮点数的下限
    :param upper: 随机浮点数的上限
    :param decimals: 小数位数（四舍五入），必须为非负整数
    :return: 随机浮点数列表
    :raises ValueError: 当参数无效时抛出
    """
    if n <= 0:
        raise ValueError("n 必须为正整数")
    if lower > upper:
        raise ValueError("lower 不能大于 upper")
    if decimals < 0:
        raise ValueError("decimals 必须为非负整数")
    return [round(random.uniform(lower, upper), decimals) for _ in range(n)]
