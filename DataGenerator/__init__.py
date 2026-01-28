"""
DataGenerator 顶层包：统一导出常用子包能力（轻量聚合）。
"""

from .PersonInfo import (
    generate_unique_names,
    generate_unique_id_numbers,
    parse_birth_ymd_from_id,
    generate_home_addresses,
    generate_ethnic_sample,
)
from .Content import (
    random_string,
    random_strings,
    DocumentGeneratorConfig,
    generate_document,
    generate_documents,
    generate_coherent_text,
)
from .DateTime import generate_date_range, generate_date
from .Numerical import generate_random_integers, generate_random_floats, generate_boolean_sequence
from .Certificate import generate_rsa_private_key

__all__ = [
    "generate_unique_names",
    "generate_unique_id_numbers",
    "parse_birth_ymd_from_id",
    "generate_home_addresses",
    "generate_ethnic_sample",
    "random_string",
    "random_strings",
    "DocumentGeneratorConfig",
    "generate_document",
    "generate_documents",
    "generate_coherent_text",
    "generate_date_range",
    "generate_date",
    "generate_random_integers",
    "generate_random_floats",
    "generate_boolean_sequence",
    "generate_rsa_private_key",
]
