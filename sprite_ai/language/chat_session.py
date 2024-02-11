from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Callable

from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.chat_state import ChatState
from sprite_ai.language.language_model import LanguageModel


class ChatSession:
    def __init__(
        self,
        chat_state: ChatState | None = None,
    ) -> None:
        if chat_state is None:
            chat_state = ChatState()
        self.chat_state = chat_state

    def add_message(self, message: ChatMessage):
        self.chat_state.chat_history.append(message)

    @property
    def messages(self):
        return self.chat_state.chat_history

    def save_state(self, state_location: str | Path):
        self.chat_state.to_file(state_location)

    def load_state(self, state_location: str | Path):
        self.chat_state = ChatState.from_file(state_location)

    def clear_state(self):
        self.chat_state = ChatState()
