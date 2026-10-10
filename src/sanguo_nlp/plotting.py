"""统一的绘图样式与中文字体配置。"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib import font_manager

_CANDIDATES = [
    "Arial Unicode MS",
    "PingFang SC",
    "Heiti SC",
    "STHeiti",
    "SimHei",
    "Microsoft YaHei",
    "Noto Sans CJK SC",
]


def use_chinese_font() -> str | None:
    """选择一种系统中可用的中文字体，返回字体名。"""
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in _CANDIDATES:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name]
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 110
    plt.rcParams["savefig.bbox"] = "tight"
    return plt.rcParams["font.sans-serif"][0] if plt.rcParams["font.sans-serif"] else None
