import pytest
from pydantic import ValidationError

from document_research.config import ModelConfig, load_model_config


def test_offline_default():
    assert load_model_config().provider is None


@pytest.mark.parametrize("provider", ["openai", "llama", "granite", "future-provider"])
def test_vendor_neutral_configuration(provider):
    config = ModelConfig(
        provider=provider, model_id=" example-model ", generation={"max_tokens": 64}
    )
    assert config.model_id == "example-model"
    assert config.generation.max_tokens == 64


@pytest.mark.parametrize(
    "values",
    [
        {"provider": "example"},
        {"model_id": "example"},
        {"provider": " ", "model_id": "example"},
        {"provider": "example", "model_id": " "},
        {"generation": {"temperature": 1}},
        {"provider": "x", "model_id": "y", "generation": {"temperature": -1}},
        {"provider": "x", "model_id": "y", "generation": {"temperature": float("nan")}},
        {"provider": "x", "model_id": "y", "generation": {"top_p": 0}},
        {"provider": "x", "model_id": "y", "generation": {"top_p": 1.1}},
        {"provider": "x", "model_id": "y", "generation": {"max_tokens": 0}},
        {"provider": "x", "model_id": "y", "generation": {"max_tokens": True}},
        {"provider": "x", "model_id": "y", "generation": {"unknown": 1}},
        {"api_key": "not-a-real-key"},
    ],
)
def test_invalid_configuration(values):
    with pytest.raises(ValidationError):
        ModelConfig.model_validate(values)


def test_json_configuration(tmp_path):
    path = tmp_path / "config.json"
    path.write_text('{"provider": "example", "model_id": "example-model"}')
    assert load_model_config(str(path)).provider == "example"
