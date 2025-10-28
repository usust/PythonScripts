from __future__ import annotations

import random
import string
from typing import List, Sequence


DEFAULT_CHARSET: Sequence[str] = tuple(string.ascii_letters + string.digits)


def random_string(
    max_length: int,
    *,
    min_length: int = 0,
    charset: Sequence[str] = DEFAULT_CHARSET,
    seed: int | None = None,
) -> str:
    """
    生成一个长度不超过 max_length 的随机字符串。

    参数:
        max_length: 随机字符串的最大长度，必须为正整数。
    关键字参数:
        min_length: 随机字符串的最小长度，默认 0。
        charset: 可选字符集，默认包含大小写字母及数字。
        seed: 可选随机种子，用于复现。

    返回:
        随机字符串，如果 max_length > 0，长度将在 [0, max_length] 区间随机。

    异常:
        ValueError: 当长度范围非法或字符集为空时抛出。
    """
    if max_length <= 0:
        raise ValueError("max_length 必须为正整数")
    if min_length < 0:
        raise ValueError("min_length 不能为负数")
    if min_length > max_length:
        raise ValueError("min_length 不能大于 max_length")
    if not charset:
        raise ValueError("charset 不能为空")

    rng = random.Random(seed)
    length = rng.randint(min_length, max_length)
    return "".join(rng.choice(charset) for _ in range(length))


def random_strings(
    count: int,
    max_length: int,
    *,
    min_length: int = 0,
    charset: Sequence[str] = DEFAULT_CHARSET,
    seed: int | None = None,
) -> List[str]:
    """
    批量生成随机字符串，每个元素长度均不超过 max_length。

    参数:
        count: 需要生成的字符串数量，必须为正整数。
        max_length: 每个字符串的最大长度，必须为正整数。
    关键字参数:
        min_length: 每个字符串的最小长度，默认 0。
        charset: 可选字符集，默认包含大小写字母及数字。
        seed: 可选随机种子，用于复现。

    返回:
        随机字符串列表。

    异常:
        ValueError: 当参数非法或字符集为空时抛出。
    """
    if count <= 0:
        raise ValueError("count 必须为正整数")
    if max_length <= 0:
        raise ValueError("max_length 必须为正整数")
    if min_length < 0:
        raise ValueError("min_length 不能为负数")
    if min_length > max_length:
        raise ValueError("min_length 不能大于 max_length")
    if not charset:
        raise ValueError("charset 不能为空")

    rng = random.Random(seed)
    return [
        random_string(
            max_length,
            min_length=min_length,
            charset=charset,
            seed=rng.randint(0, 1_000_000_000),
        )
        for _ in range(count)
    ]
