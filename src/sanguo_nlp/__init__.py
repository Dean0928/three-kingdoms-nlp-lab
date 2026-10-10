"""《三国演义》Python 与自然语言处理实验工具包。"""
from .cooccurrence import (
    build_graph,
    centrality_table,
    chapter_presence,
    cooccurrence_edges,
)
from .coherency import style_features
from .corpus import clean_text, load_chapters, read_raw, split_chapters
from .lexicons import load_aliases, load_stopwords, load_topics
from .mentions import count_mentions, count_mentions_by_chapter
from .paths import (
    DATA_DIR,
    FIGURES_DIR,
    LEXICON_DIR,
    OUTPUTS_DIR,
    RAW_DIR,
    ROOT,
    TABLES_DIR,
    ensure_output_dirs,
)
from .similarity import build_tfidf, keywords_table, similarity_pairs, top_keywords
from .text import cut, filter_words
from .topics import count_topics

__version__ = "1.0.0"

__all__ = [
    "ROOT", "DATA_DIR", "RAW_DIR", "LEXICON_DIR", "OUTPUTS_DIR",
    "FIGURES_DIR", "TABLES_DIR", "ensure_output_dirs",
    "read_raw", "clean_text", "split_chapters", "load_chapters",
    "load_aliases", "load_topics", "load_stopwords",
    "cut", "filter_words",
    "count_mentions", "count_mentions_by_chapter",
    "count_topics",
    "chapter_presence", "cooccurrence_edges", "build_graph", "centrality_table",
    "build_tfidf", "top_keywords", "keywords_table", "similarity_pairs",
    "style_features",
    "__version__",
]
