"""Run with: uv run streamlit run app.py."""

import os
from pathlib import Path

import streamlit as st
from pydantic import ValidationError

from document_research.agent import build_graph
from document_research.config import load_model_config
from document_research.ingestion import load_document

st.set_page_config(page_title="Document Research Assistant")
st.title("Agentic Document Research Assistant")
st.info(
    "Application scaffold: retrieval and model integrations are pending. No LLM calls are made."
)

try:
    config = load_model_config(os.getenv("DOCUMENT_RESEARCH_CONFIG"))
except (OSError, ValidationError) as exc:
    st.error(f"Invalid model configuration: {exc}")
    st.stop()

st.caption(
    f"Configured model: {config.provider} / {config.model_id} (integration pending)"
    if config.provider
    else "Model provider: unconfigured. The scaffold runs offline."
)
sample = Path(__file__).parent / "data" / "samples" / "procurement_policy.md"
with st.expander("Synthetic procurement policy", expanded=True):
    st.markdown(load_document(sample))

question = st.text_input("Research question")
if st.button("Prepare research", disabled=not question.strip()):
    result = build_graph().invoke({"question": question, "status": "pending", "message": ""})
    st.success(result["message"])
    st.write(f"Status: {result['status']}")
