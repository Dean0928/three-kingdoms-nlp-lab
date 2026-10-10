"""全文一致性（风格断裂）分析的语言特征工程。"""
from __future__ import annotations

import re

import jieba.posseg as pseg
import numpy as np
import pandas as pd

FUNCTION_WORDS = list("之乎者也矣焉而则乃其于以为与")
PUNCTUATIONS = ["，", "。", "！", "？", "；", "："]
POS_FEATURES = {"n": "名词占比", "v": "动词占比", "a": "形容词占比"}


def style_features(chapters: pd.DataFrame, text_col: str = "正文") -> pd.DataFrame:
    """为每一回提取词汇、句长、虚词、标点与词性特征。"""
    records = []
    for _, row in chapters.iterrows():
        text = row[text_col]
        total = len(text) or 1
        tagged = pseg.lcut(text)
        tokens = [word for word, _ in tagged if word.strip()]
        token_total = len(tokens) or 1
        sentences = [s for s in re.split(r"[。！？\n]", text) if s.strip()]

        record: dict[str, float] = {
            "章号": int(row["章号"]),
            "TTR": len(set(tokens)) / token_total,
            "平均句长": float(np.mean([len(s) for s in sentences])) if sentences else 0.0,
        }
        for char in FUNCTION_WORDS:
            record[f"虚词_{char}"] = text.count(char) / total * 100
        for punct in PUNCTUATIONS:
            record[f"标点_{punct}"] = text.count(punct) / total * 100
        for prefix, label in POS_FEATURES.items():
            record[label] = sum(1 for _, flag in tagged if flag.startswith(prefix)) / token_total
        records.append(record)
    return pd.DataFrame(records)
