"""
Content 子包：文本内容相关的常用生成函数集中导出。
"""

from .random_string import random_string, random_strings
from .document import DocumentGeneratorConfig, generate_document, generate_documents
from .sentence import generate_coherent_text

__all__ = [
    "random_string",
    "random_strings",
    "DocumentGeneratorConfig",
    "generate_document",
    "generate_documents",
    "generate_coherent_text",
]
