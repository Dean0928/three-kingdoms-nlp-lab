"""人物共现网络：边表、网络图与中心性。"""
from __future__ import annotations

from itertools import combinations

import networkx as nx
import pandas as pd

from .mentions import build_patterns


def chapter_presence(
    chapters: pd.DataFrame,
    aliases: dict[str, list[str]],
    text_col: str = "正文",
) -> list[dict]:
    """返回每一章出现（去重）的人物集合。"""
    patterns = build_patterns(aliases)
    presence = []
    for _, row in chapters.iterrows():
        names = [name for name, pattern in patterns.items() if pattern.search(row[text_col])]
        presence.append({"章号": int(row["章号"]), "人物": names})
    return presence


def cooccurrence_edges(
    chapters: pd.DataFrame,
    aliases: dict[str, list[str]],
    text_col: str = "正文",
) -> pd.DataFrame:
    """同章窗口下的人物共现边表。"""
    counter: dict[tuple[str, str], int] = {}
    for row in chapter_presence(chapters, aliases, text_col):
        for a, b in combinations(sorted(set(row["人物"])), 2):
            counter[(a, b)] = counter.get((a, b), 0) + 1
    edges = pd.DataFrame(
        [(a, b, count) for (a, b), count in counter.items()],
        columns=["人物A", "人物B", "共现次数"],
    )
    return edges.sort_values(
        ["共现次数", "人物A", "人物B"], ascending=[False, True, True]
    ).reset_index(drop=True)


def build_graph(edges: pd.DataFrame) -> nx.Graph:
    """把边表转换为无向加权图。"""
    graph = nx.Graph()
    for _, row in edges.iterrows():
        graph.add_edge(row["人物A"], row["人物B"], weight=int(row["共现次数"]))
    return graph


def centrality_table(graph: nx.Graph) -> pd.DataFrame:
    """度中心性、加权度与归一化加权度。"""
    degree = nx.degree_centrality(graph)
    weighted = dict(graph.degree(weight="weight"))
    total = sum(weighted.values()) or 1
    frame = pd.DataFrame({"人物": list(graph.nodes())})
    frame["度中心性"] = frame["人物"].map(degree)
    frame["加权度"] = frame["人物"].map(weighted)
    frame["归一化加权度"] = frame["加权度"] / total
    return frame.sort_values("加权度", ascending=False).reset_index(drop=True)
