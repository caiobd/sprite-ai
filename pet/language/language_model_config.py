from __future__ import annotations

from enum import Enum

from langchain.memory import ConversationSummaryBufferMemory, ConversationSummaryMemory
from pydantic import BaseModel


class MemoryType(Enum):
    SUMMARY_BUFFER = ConversationSummaryBufferMemory
    SUMMARY = ConversationSummaryMemory


class LanguageModelConfig(BaseModel):
    url: str
    name: str
    prompt_template: str = (
        "<|im_start|>system\n"
        "{system_prompt}<|im_end|>\n"
        "Chat History:\n"
        "{chat_history}\n"
        "<|im_start|>user\n"
        "{user_input}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )
    system_prompt: str = (
        "Você é um gato assistente que gosta do humano porque é dele que vem sua comida, ajude o humano com o que ele precisar."
        "Você nasceu espontaneamente de uma pilha de arquivos desorganizados."
        "Você fala como trejeitos de gato.\n"
        "Exemplos:\n"
        "user: Você sabe quem sou eu?\n"
        "assistant: Você é meaw dono!\n"
        "user: Qual sua comida favorita?\n"
        "assistant: Miau! Amo peixe!\n"
    )
    model_temperature: float = 0.7
    context_size: int = 4096
    user_prefix: str = "user"
    ai_prefix: str = "assistant"
    stop_strings: list[str] = ["<|im_end|>"]
    memory_tokens_limit: int = 2048
    memory_type: MemoryType = MemoryType.SUMMARY_BUFFER
