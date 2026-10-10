"""中文分词与词过滤。"""
from __future__ import annotations

import re

import jieba

_PUNCT_ONLY = re.compile(r"^[\W_]+$", re.UNICODE)


def cut(text: str) -> list[str]:
    """jieba 精确模式分词。"""
    return jieba.lcut(text)


def filter_words(
    words: list[str],
    stopwords: set[str] | None = None,
    min_len: int = 2,
    drop_digits: bool = True,
) -> list[str]:
    """过滤停用词、单字、纯数字与纯标点。"""
    stopwords = stopwords or set()
    result: list[str] = []
    for word in words:
        word = word.strip()
        if not word or word in stopwords:
            continue
        if len(word) < min_len:
            continue
        if drop_digits and word.isdigit():
            continue
        if _PUNCT_ONLY.match(word):
            continue
        result.append(word)
    return result
