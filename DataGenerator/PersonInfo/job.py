from __future__ import annotations

from typing import List

from faker import Faker

DEFAULT_LOCALE = "zh_CN"


def generate_job_titles(
    count: int,
    *,
    locale: str = DEFAULT_LOCALE,
    seed: int | None = None,
) -> List[str]:
    """
    使用 Faker 批量生成随机职业名称。

    参数:
        count: 需要生成的职业数量，必须为正整数。
    关键字参数:
        locale: Faker 使用的语言环境，默认 zh_CN。
        seed: 可选随机种子，用于结果复现。

    返回:
        职业名称列表。

    异常:
        ValueError: 当 count <= 0 时抛出；其他异常由 Faker 抛出。
    """
    if count <= 0:
        raise ValueError("count 必须为正整数")

    fake = Faker(locale)
    if seed is not None:
        fake.seed_instance(seed)

    return [fake.job() for _ in range(count)]


def generate_employer_names(
    count: int,
    *,
    locale: str = DEFAULT_LOCALE,
    seed: int | None = None,
) -> List[str]:
    """
    使用 Faker 批量生成随机工作单位名称。

    参数:
        count: 需要生成的单位数量，必须为正整数。
    关键字参数:
        locale: Faker 使用的语言环境，默认 zh_CN。
        seed: 可选随机种子，用于结果复现。

    返回:
        工作单位名称列表。

    异常:
        ValueError: 当 count <= 0 时抛出；其他异常由 Faker 抛出。
    """
    if count <= 0:
        raise ValueError("count 必须为正整数")

    fake = Faker(locale)
    if seed is not None:
        fake.seed_instance(seed)

    return [fake.company() for _ in range(count)]
