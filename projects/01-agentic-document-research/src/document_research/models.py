"""Minimal contract for future adapters; initialization stays outside orchestration."""

from typing import Protocol


class TextModel(Protocol):
    def invoke(self, prompt: str) -> str:
        """Generate text; future integrations map their SDK responses to a string."""
        ...
