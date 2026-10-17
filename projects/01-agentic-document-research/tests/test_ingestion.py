from pathlib import Path

import pytest

from document_research.ingestion import load_document


def test_sample():
    sample = Path(__file__).resolve().parents[1] / "data/samples/procurement_policy.md"
    text = load_document(sample)
    assert "Synthetic demonstration data" in text
    assert "three vendor quotes" in text


def test_missing_document(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_document(tmp_path / "missing.md")
