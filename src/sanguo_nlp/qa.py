"""可追溯问答：每个答案都附带数据来源。"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .paths import TABLES_DIR


def _markdown_table(frame: pd.DataFrame) -> str:
    """不依赖 tabulate 的简易 Markdown 表格。"""
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for record in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in record) + " |")
    return "\n".join(lines)


class SanguoQA:
    """基于前面实验产出的中间结果回答问题的“小型分析助手”。

    设计原则：只读 outputs/tables/ 中已经生成的表格，绝不凭空生成统计值。
    """

    def __init__(self, tables_dir: str | Path | None = None):
        self.tables_dir = Path(tables_dir) if tables_dir else TABLES_DIR
        self.character_frequencies = self._read("character_frequencies.csv")
        self.character_trends = self._read("character_trends.csv")
        self.edges = self._read("character_cooccurrence_edges.csv")
        self.keywords = self._read("chapter_tfidf_keywords.csv")
        self.similarity = self._read("chapter_similarity.csv")
        self.topics = self._read("topic_trends.csv")

    def _read(self, name: str) -> pd.DataFrame:
        return pd.read_csv(self.tables_dir / name, encoding="utf-8-sig")

    def who_appears_most(self, top_n: int = 5):
        answer = self.character_frequencies.head(top_n).reset_index(drop=True)
        cross_check = (
            self.character_trends.drop(columns=["章号"]).sum().sort_values(ascending=False)
        )
        evidence = (
            "依据 outputs/tables/character_frequencies.csv（别名归一后全书提及次数）；"
            "可用 outputs/tables/character_trends.csv 的逐章求和交叉验证："
            + "、".join(f"{k}={int(v)}" for k, v in cross_check.head(top_n).items())
        )
        return answer, evidence

    def most_active_chapters(self, person: str, top_n: int = 5):
        if person not in self.character_trends.columns:
            return None, f"outputs/tables/character_trends.csv 中没有人物 {person}。"
        answer = (
            self.character_trends[["章号", person]]
            .nlargest(top_n, person)
            .reset_index(drop=True)
        )
        evidence = (
            f"依据 outputs/tables/character_trends.csv 中 {person} 列按章统计的出场次数"
            "（别名归一 + 长别名优先匹配）。"
        )
        return answer, evidence

    def cooccur_with(self, person: str, top_n: int = 5):
        related = self.edges[(self.edges["人物A"] == person) | (self.edges["人物B"] == person)]
        if related.empty:
            return None, f"outputs/tables/character_cooccurrence_edges.csv 中没有人物 {person}。"
        related = related.copy()
        related["共现人物"] = related.apply(
            lambda row: row["人物A"] if row["人物B"] == person else row["人物B"], axis=1
        )
        answer = related.nlargest(top_n, "共现次数")[["共现人物", "共现次数"]].reset_index(drop=True)
        evidence = (
            "依据 outputs/tables/character_cooccurrence_edges.csv（同章共现窗口，"
            f"统计与 {person} 同章出现的次数）。"
        )
        return answer, evidence

    def similar_chapters(self, chapter: int, top_n: int = 5):
        related = self.similarity[
            (self.similarity["章号A"] == chapter) | (self.similarity["章号B"] == chapter)
        ]
        if related.empty:
            return None, f"outputs/tables/chapter_similarity.csv 中没有第 {chapter} 回。"
        related = related.copy()
        related["相似章节"] = related.apply(
            lambda row: row["章号A"] if row["章号B"] == chapter else row["章号B"], axis=1
        )
        answer = related.nlargest(top_n, "相似度")[["相似章节", "相似度"]].reset_index(drop=True)
        answer["相似章节"] = answer["相似章节"].astype(int)
        evidence = (
            "依据 outputs/tables/chapter_similarity.csv（TF-IDF 余弦相似度，"
            f"第 {chapter} 回与其它各回两两比较）。"
        )
        return answer, evidence

    def war_chapters(self, top_n: int = 5):
        if "战争" not in self.topics.columns:
            return None, "outputs/tables/topic_trends.csv 中没有“战争”主题列。"
        answer = self.topics.nlargest(top_n, "战争")[["章号", "战争", "战争_占比"]].reset_index(drop=True)
        answer["章号"] = answer["章号"].astype(int)
        evidence = (
            "依据 outputs/tables/topic_trends.csv，按“战争”主题关键词计数排序"
            "（词典见 data/lexicons/topic_lexicon.json）。"
        )
        return answer, evidence

    def report(self, questions) -> str:
        """把多个问题整理成 Markdown 报告。"""
        lines = ["# 《三国演义》可追溯问答报告", ""]
        for title, result, evidence in questions:
            lines.append(f"## {title}")
            lines.append("")
            lines.append("- 无法回答。" if result is None else _markdown_table(result))
            lines.append("")
            lines.append(f"**依据：** {evidence}")
            lines.append("")
        return "\n".join(lines)
