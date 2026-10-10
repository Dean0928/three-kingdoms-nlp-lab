"""人物提及统计：正则 + 别名归一。"""
from __future__ import annotations

import re

import pandas as pd


def build_patterns(aliases: dict[str, list[str]]) -> dict[str, re.Pattern]:
    """为每个人物编译 “长别名优先” 的正则，避免子串重复计数。"""
    patterns: dict[str, re.Pattern] = {}
    for name, values in aliases.items():
        ordered = sorted(values, key=len, reverse=True)
        patterns[name] = re.compile("|".join(re.escape(value) for value in ordered))
    return patterns


def count_mentions(text: str, aliases: dict[str, list[str]]) -> dict[str, int]:
    """统计全书各人物提及次数。"""
    patterns = build_patterns(aliases)
    return {name: len(pattern.findall(text)) for name, pattern in patterns.items()}


def count_mentions_by_chapter(
    chapters: pd.DataFrame,
    aliases: dict[str, list[str]],
    text_col: str = "正文",
) -> pd.DataFrame:
    """按章统计各人物提及次数，返回 章号 + 每个人物一列 的宽表。"""
    patterns = build_patterns(aliases)
    records = []
    for _, row in chapters.iterrows():
        record: dict[str, int] = {"章号": int(row["章号"])}
        for name, pattern in patterns.items():
            record[name] = len(pattern.findall(row[text_col]))
        records.append(record)
    return pd.DataFrame(records)
