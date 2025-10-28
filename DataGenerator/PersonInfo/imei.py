from __future__ import annotations

from typing import List

from faker import Faker

DEFAULT_LOCALE = "zh_CN"


def generate_imei(*, locale: str = DEFAULT_LOCALE, seed: int | None = None) -> str:
    """
    使用 Faker 模块生成单个 IMEI 号码。

    参数:
        locale: Faker 的语言环境，默认 zh_CN。
        seed: 可选随机种子，用于结果复现。

    返回:
        由 Faker 生成的 15 位 IMEI 字符串。

    异常:
        Faker 本身会在 locale 或其他参数非法时抛出异常。
    """
    fake = Faker(locale)
    if seed is not None:
        fake.seed_instance(seed)

    return fake.imei()


def generate_imeis(
    count: int,
    *,
    locale: str = DEFAULT_LOCALE,
    seed: int | None = None,
) -> List[str]:
    """
    批量生成 IMEI 号码。

    参数:
        count: 需要生成的 IMEI 数量，必须为正整数。
    关键字参数:
        locale: Faker 的语言环境，默认 zh_CN。
        seed: 可选随机种子，用于结果复现。

    返回:
        IMEI 字符串列表。

    异常:
        ValueError: 当 count <= 0 时抛出；其他异常由 Faker 抛出。
    """
    if count <= 0:
        raise ValueError("count 必须为正整数")

    fake = Faker(locale)
    if seed is not None:
        fake.seed_instance(seed)

    return [fake.imei() for _ in range(count)]
