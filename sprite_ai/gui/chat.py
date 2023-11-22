import os
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable

import pyperclip
from loguru import logger
from rofi import Rofi

from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.chat_session import ChatSession
from sprite_ai.language.language_model import LanguageModel


@dataclass
class Command:
    name: str
    callback: Callable

    def __str__(self) -> str:
        return self.name


class ChatWindow:
    def __init__(
        self,
        language_model: LanguageModel,
        on_chat_message: Callable | None = None,
        on_canceled: Callable | None = None,
        persistence_location: str = "",
    ) -> None:
        # Implement command pattern here and inject commands via init
        # This allows for better extensibility and modularity
        self.commands = [
            Command("[x] exit", lambda: os._exit(0)),
            Command("+ new message", self._new_message_menu),
        ]
        self.chat_session = ChatSession(
            language_model, on_message=self._on_chat_message
        )
        self.persistence_location = persistence_location

        self._rofi = Rofi()
        self._pool = ThreadPoolExecutor()

        self.on_chat_message = on_chat_message
        self.on_canceled = on_canceled

    def load_state(self):
        self.chat_session.load_state(self.persistence_location)

    def save_state(self):
        if not self.persistence_location:
            logger.error("Error, set persistence location before saving")
        self.chat_session.save_state(self.persistence_location)

    def show(self):
        self._main_menu()

    def _on_chat_message(self, chat_message_future: Future[ChatMessage]):
        chat_message = chat_message_future.result()
        self.on_chat_message(chat_message)
        if self.persistence_location:
            self.chat_session.save_state(self.persistence_location)

    @property
    def options(self):
        options = self.chat_session.messages + self.commands
        options.reverse()
        return options

    @property
    def options_names(self):
        options = [str(option) for option in self.options]
        return options

    def _new_message_menu(self):
        last_message = ""
        chat_history = self.chat_session.messages

        if chat_history:
            last_message = str(chat_history[-1])

        user_message = self._rofi.text_entry("👷 | you", last_message)
        if user_message is None:
            self.on_canceled()
            return
        self.chat_session.send_message(user_message)

    def _main_menu(self):
        index, key = self._rofi.select("Option", self.options_names)

        if key == -1 or index == -1:
            self.on_canceled()
            return
        if index < len(self.commands):
            command = self.options[index]
            command.callback()
        else:
            selected_message = self.options[index]
            pyperclip.copy(selected_message.content)
            self.on_canceled()
