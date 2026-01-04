# coding: utf-8
from pathlib import Path

__all__ = [
    "DATA",
]

PROJECT_ROOT = Path(__file__).absolute().parent.parent
DATA = PROJECT_ROOT / "data"
