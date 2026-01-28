"""
PersonInfo 子包：对外集中暴露常用的生成函数，便于简洁导入。
"""

from .name import generate_unique_names
from .id_card import generate_unique_id_numbers, parse_birth_ymd_from_id
from .address import generate_home_addresses
from .nation import generate_ethnic_sample

__all__ = [
    "generate_unique_names",
    "generate_unique_id_numbers",
    "parse_birth_ymd_from_id",
    "generate_home_addresses",
    "generate_ethnic_sample",
]
