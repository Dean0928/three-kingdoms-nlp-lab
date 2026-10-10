"""加载停用词表、人物别名表与主题词典。"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .paths import DATA_DIR, LEXICON_DIR

ALIAS_FILE = LEXICON_DIR / "character_aliases.csv"
TOPIC_FILE = LEXICON_DIR / "topic_lexicon.json"
STOPWORDS_FILE = DATA_DIR / "stopwords_cn.txt"


def load_aliases(path: str | Path | None = None) -> dict[str, list[str]]:
    """读取人物别名表（长表：标准名, 别名），返回 标准名 -> 别名列表。"""
    frame = pd.read_csv(path or ALIAS_FILE, dtype=str, encoding="utf-8-sig").fillna("")
    aliases: dict[str, list[str]] = {}
    for _, row in frame.iterrows():
        name = str(row["标准名"]).strip()
        alias = str(row["别名"]).strip()
        if not name or not alias:
            continue
        aliases.setdefault(name, [])
        if alias not in aliases[name]:
            aliases[name].append(alias)
    # 长别名优先，避免 “刘玄德” 同时被 “玄德” 匹配而重复计数
    return {name: sorted(values, key=len, reverse=True) for name, values in aliases.items()}


def load_topics(path: str | Path | None = None) -> dict[str, list[str]]:
    """读取主题词典（JSON：主题 -> 关键词列表）。"""
    with open(path or TOPIC_FILE, encoding="utf-8") as handle:
        return json.load(handle)


def load_stopwords(path: str | Path | None = None) -> set[str]:
    """读取停用词表（每行一个词）。"""
    target = Path(path) if path else STOPWORDS_FILE
    with open(target, encoding="utf-8") as handle:
        return {line.strip() for line in handle if line.strip()}
