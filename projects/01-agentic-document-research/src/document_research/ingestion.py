"""Local text ingestion; parsing and chunking will be added in later issues."""

from pathlib import Path


def load_document(path: Path) -> str:
    return path.read_text(encoding="utf-8")
