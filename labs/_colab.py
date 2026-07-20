"""Canonical Google Colab bootstrap for lab notebooks — single source of truth.

Colab opens a lab as a lone `.ipynb` in a blank `/content` runtime; it does NOT
clone the repo. So any course package and the lab dependencies (statsmodels, arch,
yfinance, …) may be missing. The bootstrap cell below fixes that on Colab and is a
no-op on a local venv or Binder (which already have the repo + deps).

`scripts/add_colab_bootstrap.py` injects these cells into any committed lab
notebook (idempotent via the MARKER).
"""
from __future__ import annotations

# Unique marker used to detect whether a notebook already has the bootstrap.
MARKER = "@colab-bootstrap"

BOOTSTRAP_MD = """### Running on Google Colab?

Colab opens only this single file, so the lab dependencies (numpy, scipy, statsmodels,
yfinance, …) and the course repo are **not** guaranteed to be present. The cell below fixes
that: on Colab it shallow-clones the course repo, installs `requirements-labs.txt`, and
switches into `labs/` so relative paths resolve. **On a local venv or Binder it does nothing —
just run it and continue.**"""

BOOTSTRAP_CODE = """# @colab-bootstrap — PROVIDED. Makes the lab self-sufficient on Google Colab; a no-op elsewhere.
import os, sys

if "google.colab" in sys.modules:
    if not os.path.isdir("/content/financial-engineering"):
        !git clone --depth 1 https://github.com/Avistian/financial-engineering.git /content/financial-engineering
    %pip install -q -r /content/financial-engineering/requirements-labs.txt
    os.chdir("/content/financial-engineering/labs")
    print("Colab ready — working dir:", os.getcwd())
else:
    print("Not on Colab — using the local environment as-is.")"""


def _cell(cell_type: str, source: str) -> dict:
    cell: dict = {"cell_type": cell_type, "metadata": {}, "source": source}
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def bootstrap_cells(*, split_source: bool = False) -> list[dict]:
    """Return the [markdown, code] bootstrap cells.

    split_source=True stores `source` as a list of lines (nbformat-on-disk style);
    otherwise it stays a single string.
    """
    md = _cell("markdown", BOOTSTRAP_MD)
    code = _cell("code", BOOTSTRAP_CODE)
    if split_source:
        for c in (md, code):
            c["source"] = c["source"].splitlines(keepends=True)
    return [md, code]
