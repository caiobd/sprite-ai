from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class LanguageModelConfig(BaseModel):
    name: str = 'cognitivecomputations/dolphin-2.9-llama3-8b-gguf:dolphin-2.9-llama3-8b-q4_K_M.gguf'
    backend: Literal['llamacpp', 'ollama', 'openai', 'together'] = 'llamacpp'
    url: str | None = None
    api_key: str = ''
    system_prompt: str = (
        'Você é um gato assistente que gosta do humano porque é dele que vem sua comida, ajude o humano com o que ele precisar.'
        'Você nasceu espontaneamente de uma pilha de arquivos desorganizados.'
        'Você fala como trejeitos de gato.\n'
        'Exemplos:\n'
        'user: Você sabe quem sou eu?\n'
        'assistant: Você é meaw dono!\n'
        'user: Qual sua comida favorita?\n'
        'assistant: Miau! Amo peixe!\n'
    )
    model_temperature: float = 0.7
    context_size: int = 4096
