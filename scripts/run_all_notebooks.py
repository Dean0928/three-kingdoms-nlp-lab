"""按编号顺序执行 notebooks/ 下的全部实验，并把运行结果写回 notebook。

用法：
    python scripts/run_all_notebooks.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    notebooks = sorted((ROOT / "notebooks").glob("exp*.ipynb"))
    if not notebooks:
        raise SystemExit("没有找到任何 notebook")
    for notebook in notebooks:
        print(f"==> 执行 {notebook.name}", flush=True)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--inplace",
                "--ExecutePreprocessor.timeout=900",
                str(notebook),
            ],
            check=True,
        )
    print("全部 notebook 执行完成。")


if __name__ == "__main__":
    main()
