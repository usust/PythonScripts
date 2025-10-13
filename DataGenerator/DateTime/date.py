import random
from datetime import datetime, timedelta
from typing import Optional


def generate_date_range(start_date: str, end_date: str, date_format: str = "%Y-%m-%d", quantity: Optional[int] = None) -> list[str]:
    """
    返回给定起止日期（包含端点）的日期列表。

    :param start_date: 起始日期字符串，例如 "2024-01-01"
    :param end_date: 结束日期字符串，例如 "2024-01-10"
    :param date_format: 日期字符串格式，默认 "%Y-%m-%d"
    :param quantity: 需要返回的日期数量，默认返回全部；当数量超过区间长度时会随机重复日期
    :return: 日期字符串列表
    :raises ValueError: 当起始日期在结束日期之后时抛出
    :raises ValueError: 当 quantity 非正整数时抛出
    """
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    if start > end:
        raise ValueError("start_date 不能晚于 end_date")
    total_days = (end - start).days + 1
    if quantity is not None:
        if quantity <= 0:
            raise ValueError("quantity 必须为正整数")
        offsets = [random.randrange(total_days) for _ in range(quantity)]
    else:
        offsets = list(range(total_days))
        random.shuffle(offsets)
    return [(start + timedelta(days=offset)).strftime(date_format) for offset in offsets]

def generate_date(start_date: str, end_date: str, date_format: str = "%Y-%m-%d") -> str:
    """
    返回给定区间内的单个随机日期字符串。

    :param start_date: 起始日期字符串，例如 "2024-01-01"
    :param end_date: 结束日期字符串，例如 "2024-01-10"
    :param date_format: 日期字符串格式，默认 "%Y-%m-%d"
    :return: 单个随机日期字符串
    :raises ValueError: 当起始日期在结束日期之后时抛出
    """
    return generate_date_range(start_date, end_date, date_format, quantity=1)[0]