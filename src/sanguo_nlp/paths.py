"""仓库路径配置：所有数据与输出目录都相对于仓库根目录解析。"""
from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
ROOT = PACKAGE_DIR.parents[1]  # three-kingdoms-nlp-lab/

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
LEXICON_DIR = DATA_DIR / "lexicons"
OUTPUTS_DIR = ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"


def ensure_output_dirs() -> None:
    """确保输出目录存在。"""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
