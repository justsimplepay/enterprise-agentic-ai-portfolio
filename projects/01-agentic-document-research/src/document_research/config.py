"""Explicit, vendor-neutral configuration; no credentials or default provider."""

from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonBlank = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class GenerationSettings(BaseModel):
    """Portable settings; provider-specific support belongs in future integrations."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    temperature: float | None = Field(default=None, ge=0, le=2)
    top_p: float | None = Field(default=None, gt=0, le=1)
    max_tokens: int | None = Field(default=None, gt=0, strict=True)


class ModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: NonBlank | None = None
    model_id: NonBlank | None = None
    generation: GenerationSettings = Field(default_factory=GenerationSettings)

    @model_validator(mode="after")
    def require_provider_and_model(self) -> "ModelConfig":
        if (self.provider is None) != (self.model_id is None):
            raise ValueError("provider and model_id must be configured together")
        if self.provider is None and self.generation.model_dump(exclude_none=True):
            raise ValueError("generation settings require a provider and model_id")
        return self


def load_model_config(path: str | None = None) -> ModelConfig:
    """Read an optional JSON file, or return an unconfigured offline default."""
    return (
        ModelConfig.model_validate_json(Path(path).read_text(encoding="utf-8"))
        if path
        else ModelConfig()
    )
