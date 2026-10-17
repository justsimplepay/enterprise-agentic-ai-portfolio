# Agentic Document Research Assistant

An independently runnable Python 3.12 scaffold for Project 1. It previews a synthetic
procurement policy and executes a deterministic LangGraph state transition. Retrieval,
embeddings, model integrations, and tool calling are reserved for subsequent issues.
No API credentials, model downloads, external inference, or AWS resources are needed.

## Local setup

Install Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
cd projects/01-agentic-document-research
uv sync --locked
uv run streamlit run app.py --browser.gatherUsageStats=false
```

Open http://localhost:8501. Enter a question and select **Prepare research** to move
from `pending` to `ready`. The result confirms preparation; it does not answer the
question or search the policy. The policy is fictional demonstration data.

## Configuration

The application runs with no model configured. To validate a future model selection,
copy `config.example.json` to a local JSON file and set `DOCUMENT_RESEARCH_CONFIG` to
its path before starting Streamlit. For example, the file may contain:

```json
{
  "provider": "your-provider",
  "model_id": "your-model-identifier",
  "generation": {"temperature": 0.2, "top_p": 0.9, "max_tokens": 256}
}
```

Provider and model identifier must be supplied together and must not be blank.
Generation settings are optional: temperature is 0–2, top_p is greater than 0 and
at most 1, and max_tokens is a positive integer. Unknown fields and non-finite
numbers are rejected. These are portable configuration bounds; future adapters
must validate which settings their chosen model actually supports. Configuration
does not initialize or invoke a provider. Do not put secrets in this file.

## Components

- `app.py`: Streamlit UI, configuration validation, sample preview, graph invocation.
- `src/document_research/config.py`: Pydantic configuration and optional JSON loader.
- `models.py`: one `TextModel` protocol (`invoke(str) -> str`) for future adapters.
  There is no factory, registry, or provider implementation. Future initialization
  belongs outside orchestration; the deterministic graph needs no model today.
- `agent.py`: `START → prepare → END`; trims and validates a question, then marks
  the request ready. No LLM or tool calls are made.
- `ingestion.py`: UTF-8 text loading. Parsing and chunking are deferred.
- `retrieval.py`: explicit unimplemented retrieval boundary; no database is opened.
- `tools.py`: reserved module; no tools are registered.
- `data/samples/`: one synthetic procurement policy.

Streamlit supplies the UI; LangGraph supplies graph execution; LangChain supplies
future LLM building blocks; ChromaDB is included for later retrieval work; Pydantic
validates configuration. No ChromaDB client or embedding model is initialized.
The project has its own `pyproject.toml`, Python version, and committed `uv.lock`.

## Verification

```sh
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Tests cover valid/invalid model configuration, local document loading, deterministic
graph execution, and Streamlit UI startup and interaction using `AppTest`.
GitHub Actions runs these checks and starts a headless Streamlit server, checks its
health endpoint, then stops it. No credentials are needed for CI. Usage reporting
is disabled for the startup check.
