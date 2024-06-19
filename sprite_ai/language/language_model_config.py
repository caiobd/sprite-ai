from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class LanguageModelConfig(BaseModel):
    name: str = 'cognitivecomputations/dolphin-2.9-llama3-8b-gguf:dolphin-2.9-llama3-8b-q4_K_M.gguf'
    backend: Literal['llamacpp', 'ollama', 'openai', 'together'] = 'llamacpp'
    url: str | None = None
    api_key: str = 'NULL'
    model_temperature: float = 0.7
    context_size: int = 4096
