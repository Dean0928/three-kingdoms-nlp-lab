"""TF-IDF 关键词提取与章节相似度。"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_tfidf(
    documents,
    max_features: int = 1000,
    min_df: int = 2,
    max_df: float = 0.8,
):
    """构建 TF-IDF 矩阵，返回 (矩阵, 词表)。"""
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        min_df=min_df,
        max_df=max_df,
        token_pattern=r"(?u)\b\w+\b",
    )
    matrix = vectorizer.fit_transform(documents)
    return matrix, vectorizer.get_feature_names_out()


def top_keywords(matrix, terms, row_index: int, top_k: int = 10):
    """取某一行（章）TF-IDF 权重最高的关键词。"""
    row = np.asarray(matrix[row_index].todense()).ravel()
    order = row.argsort()[::-1]
    return [(terms[i], float(row[i])) for i in order if row[i] > 0][:top_k]


def keywords_table(matrix, terms, chapter_numbers, top_k: int = 10) -> pd.DataFrame:
    """为每一章提取关键词，返回长表。"""
    records = []
    for row_index, chapter in enumerate(chapter_numbers):
        for word, weight in top_keywords(matrix, terms, row_index, top_k):
            records.append({"章号": int(chapter), "关键词": word, "TF-IDF权重": round(weight, 6)})
    return pd.DataFrame(records)


def similarity_pairs(matrix):
    """返回余弦相似度矩阵与所有章节对（按相似度降序）。"""
    matrix_sim = cosine_similarity(matrix)
    pairs = [
        (i + 1, j + 1, float(matrix_sim[i, j]))
        for i in range(matrix_sim.shape[0])
        for j in range(i + 1, matrix_sim.shape[1])
    ]
    pairs.sort(key=lambda item: item[2], reverse=True)
    return matrix_sim, pd.DataFrame(pairs, columns=["章号A", "章号B", "相似度"])
