"""不依赖 notebook，直接从命令行跑通“清洗 -> 统计 -> 图表”的最小流程。

该脚本演示如何把 src/sanguo_nlp 当作普通 Python 包复用；完整的实验过程请看 notebooks/。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sanguo_nlp import load_aliases, load_chapters  # noqa: E402
from sanguo_nlp.cooccurrence import cooccurrence_edges  # noqa: E402
from sanguo_nlp.mentions import count_mentions_by_chapter  # noqa: E402
from sanguo_nlp.paths import TABLES_DIR, ensure_output_dirs  # noqa: E402


def main() -> None:
    ensure_output_dirs()
    chapters = load_chapters()
    aliases = load_aliases()

    trends = count_mentions_by_chapter(chapters, aliases)
    trends.to_csv(TABLES_DIR / "character_trends.csv", index=False, encoding="utf-8-sig")

    edges = cooccurrence_edges(chapters, aliases)
    edges.to_csv(
        TABLES_DIR / "character_cooccurrence_edges.csv", index=False, encoding="utf-8-sig"
    )

    print(f"章节数: {len(chapters)}")
    print(f"人物数: {len(aliases)}")
    print(f"共现边数: {len(edges)}")
    print(f"输出目录: {TABLES_DIR}")


if __name__ == "__main__":
    main()
