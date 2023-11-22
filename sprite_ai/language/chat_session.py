from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Callable

from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.chat_state import ChatState
from sprite_ai.language.language_model import LanguageModel


class ChatSession:
    def __init__(
        self,
        language_model: LanguageModel,
        chat_state: ChatState | None = None,
        on_message: Callable | None = None,
    ) -> None:
        if chat_state is None:
            chat_state = ChatState()
        self.language_model = language_model
        self.chat_state = chat_state
        self.on_message = on_message
        self._pool = ThreadPoolExecutor()

    def send_message(self, message: str):
        chat_message = ChatMessage(sender="👷 | you", content=message)
        self.chat_state.chat_history.append(chat_message)

        message_future = self._pool.submit(
            self.language_model.awnser, chat_message.content
        )
        message_future.add_done_callback(self._log_chat_awnser)
        if self.on_message is not None:
            message_future.add_done_callback(self.on_message)

    def _log_chat_awnser(self, message_future: Future):
        message: str = message_future.result()
        chat_message_awnser = ChatMessage(sender="😸 | cat", content=message)
        self.chat_state.chat_history.append(chat_message_awnser)

    @property
    def messages(self):
        return self.chat_state.chat_history

    def save_state(self, persistence_location: str):
        persistence_location: Path = Path(persistence_location)

        persistence_location.mkdir(parents=True, exist_ok=True)
        chat_state_location = persistence_location / "state.yml"
        language_model_memory_location = persistence_location / "state.mem"

        self.chat_state.to_file(chat_state_location)
        self.language_model.save_memory(language_model_memory_location)

    def load_state(self, persistence_location: str):
        persistence_location = Path(persistence_location)

        chat_state_location = persistence_location / "state.yml"
        language_model_memory_location = persistence_location / "state.mem"

        self.chat_state = ChatState.from_file(chat_state_location)
        self.language_model.load_memory(language_model_memory_location)
