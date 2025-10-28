from __future__ import annotations

import random
from typing import Iterable, List


SUPPORTED_BANK_IDENTIFIERS: tuple[str, ...] = (
    "622202",  # 工商银行
    "622848",  # 农业银行
    "622700",  # 建设银行
    "622588",  # 交通银行
    "622262",  # 中国银行
    "621098",  # 招商银行
    "622155",  # 民生银行
    "622689",  # 广发银行
    "622318",  # 光大银行
    "622908",  # 中信银行
)


def generate_bank_card_number(
    *,
    issuer_identifiers: Iterable[str] = SUPPORTED_BANK_IDENTIFIERS,
    length: int = 16,
    seed: int | None = None,
) -> str:
    """
    生成一个符合 Luhn 校验的银行卡号。

    参数:
        issuer_identifiers: 发行方识别号（IIN/BIN）集合，用于确定开头前缀。
        length: 银行卡总长度（含校验位），通常是 16 或 19。
    关键字参数:
        seed: 可选随机种子，便于复现。

    返回:
        单个银行卡号字符串。

    异常:
        ValueError: 当参数非法或无法生成号码时抛出。
    """
    issuer_identifiers = tuple(issuer_identifiers)
    if not issuer_identifiers:
        raise ValueError("issuer_identifiers 不能为空")
    if length not in (13, 14, 15, 16, 17, 18, 19):
        raise ValueError("银行卡长度须在 13~19 位之间")

    rng = random.Random(seed)
    prefix = rng.choice(issuer_identifiers)
    if not prefix.isdigit():
        raise ValueError("issuer_identifiers 中的元素必须为数字字符串")
    if len(prefix) >= length:
        raise ValueError("发行方识别号长度必须小于卡号总长度")

    body_length = length - len(prefix) - 1
    body_digits = "".join(rng.choice("0123456789") for _ in range(body_length))
    partial_number = prefix + body_digits

    check_digit = _compute_luhn_check_digit(partial_number)
    return partial_number + check_digit


def generate_bank_card_numbers(
    count: int,
    *,
    issuer_identifiers: Iterable[str] = SUPPORTED_BANK_IDENTIFIERS,
    length: int = 16,
    seed: int | None = None,
) -> List[str]:
    """
    批量生成银行卡号。

    参数:
        count: 需要生成的银行卡号数量。
    关键字参数:
        issuer_identifiers: 发行方识别号（IIN/BIN）集合。
        length: 银行卡总长度。
        seed: 可选随机种子。

    返回:
        银行卡号字符串列表。

    异常:
        ValueError: 当参数非法时抛出。
    """
    if count <= 0:
        raise ValueError("count 必须为正整数")

    rng = random.Random(seed)
    return [
        generate_bank_card_number(
            issuer_identifiers=issuer_identifiers,
            length=length,
            seed=rng.randint(0, 1_000_000_000),
        )
        for _ in range(count)
    ]


def _compute_luhn_check_digit(number: str) -> str:
    """
    根据 Luhn 算法计算校验位。
    """
    total = 0
    reverse_digits = number[::-1]
    for index, digit_char in enumerate(reverse_digits, start=1):
        digit = int(digit_char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)
