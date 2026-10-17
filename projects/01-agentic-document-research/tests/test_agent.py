import pytest

from document_research.agent import build_graph


def test_deterministic_transition():
    graph = build_graph()
    initial = {"question": "  Who approves purchases?  ", "status": "pending", "message": ""}
    result = graph.invoke(initial)
    assert result["question"] == "Who approves purchases?"
    assert result["status"] == "ready"
    assert "integration are pending" in result["message"]
    assert graph.invoke(initial) == result
    assert initial["status"] == "pending"


def test_blank_question():
    with pytest.raises(ValueError, match="blank"):
        build_graph().invoke({"question": " ", "status": "pending", "message": ""})
