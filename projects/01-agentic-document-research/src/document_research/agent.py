"""Deterministic LangGraph scaffold. No model or tool calls are made."""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class ResearchState(TypedDict):
    question: str
    status: Literal["pending", "ready"]
    message: str


def prepare_research(state: ResearchState) -> dict:
    question = state["question"].strip()
    if not question:
        raise ValueError("question must not be blank")
    return {
        "question": question,
        "status": "ready",
        "message": "Research request prepared. Retrieval and model integration are pending.",
    }


def build_graph():
    """Compile a single state transition, independent of any model provider."""
    graph = StateGraph(ResearchState)
    graph.add_node("prepare", prepare_research)
    graph.add_edge(START, "prepare")
    graph.add_edge("prepare", END)
    return graph.compile()
