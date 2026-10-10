"""语料读取、清洗与按“回”切分。"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .paths import RAW_DIR

CORPUS_FILE = RAW_DIR / "sanguoyanyi.txt"

# 只匹配“行首”的回目标记，避免正文中引用“第X回”造成误切分
CHAPTER_HEADING = re.compile(
    r"^[ \t]*第([一二三四五六七八九十百千零0-9]+)回", re.MULTILINE
)

# 语料第40回结尾混入了一处目录式残留：“#第四十一回\n标题A\n标题B+正文”
# 该规则删除 “#第X回” 以及紧随其后的两行标题，但保留正文。
_MARKDOWN_RESIDUE = re.compile(
    r"#第[一二三四五六七八九十百千零0-9]+回\s*\n"
    r"(?:[^\n]{1,12}\n)?"
    r"[^\n]{0,12}(?=(?:却说|且说|话说|未知|且看))"
)


def read_raw(path: str | Path | None = None) -> str:
    """按 UTF-8 读取原始语料。"""
    target = Path(path) if path else CORPUS_FILE
    return target.read_text(encoding="utf-8")


def clean_text(text: str) -> str:
    """统一的清洗规则，便于在实验记录中复述。

    1. 去掉 UTF-8 BOM；
    2. 统一换行符为 \n；
    3. 全角空格替换为半角空格；
    4. 删除目录式残留标记；
    5. 合并连续空格与空行。
    """
    text = text.lstrip("\ufeff")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u3000", " ")
    text = _MARKDOWN_RESIDUE.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def split_chapters(text: str) -> pd.DataFrame:
    """把整书文本切分为章节表：章号 / 回目 / 标题 / 正文。"""
    cleaned = clean_text(text)
    matches = list(CHAPTER_HEADING.finditer(cleaned))
    rows = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(cleaned)
        segment = cleaned[match.end():end]
        title, _, body = segment.partition("\n")
        rows.append(
            {
                "章号": i + 1,
                "回目": match.group(0).strip(),
                "标题": title.strip(),
                "正文": body.strip(),
            }
        )
    return pd.DataFrame(rows)


def load_chapters(path: str | Path | None = None) -> pd.DataFrame:
    """读取原始语料并返回章节表（最常用的入口）。"""
    return split_chapters(read_raw(path))
