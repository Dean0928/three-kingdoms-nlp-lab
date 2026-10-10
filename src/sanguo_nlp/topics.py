"""主题词典法统计。"""
from __future__ import annotations

import pandas as pd


def count_topics(
    chapters: pd.DataFrame,
    topics: dict[str, list[str]],
    text_col: str = "正文",
) -> pd.DataFrame:
    """按章统计每个主题的关键词出现次数与占比。

    一个词允许同时计入多个主题（重叠计数），因为《三国演义》中一词多义、
    跨主题的词语占比很小，重叠计数对整体趋势影响有限。
    """
    records = []
    for _, row in chapters.iterrows():
        text = row[text_col]
        record: dict[str, float] = {"章号": int(row["章号"]), "总字符数": len(text)}
        for topic, keywords in topics.items():
            record[topic] = sum(text.count(keyword) for keyword in keywords)
        records.append(record)
    frame = pd.DataFrame(records)
    for topic in topics:
        frame[f"{topic}_占比"] = frame[topic] / frame["总字符数"]
    return frame
