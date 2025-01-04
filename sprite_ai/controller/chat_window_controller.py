from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from time import time
from typing import Callable

from loguru import logger
import texteditor

from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.chat_session import ChatSession
from sprite_ai.ui.chat_window import ChatWindow


class ChatWindowController:
    def __init__(
        self,
        settings_location: str | Path,
        on_exit: Callable,
        on_user_message: Callable | None = None,
        on_assistant_message: Callable | None = None,
        on_clear_chat: Callable | None = None,
    ) -> None:
        self.chat_window = ChatWindow(
            on_clear_chat=self.clear_chat_session,
            on_user_message=self.process_user_message,
            on_open_settings=self.open_settings,
            on_exit=on_exit,
        )
        self.settings_location = Path(settings_location)

        self.chat_session = ChatSession()
        self._pool = ThreadPoolExecutor()
        self.on_user_message = on_user_message
        self.on_assistant_message = on_assistant_message
        self.on_clear_chat = on_clear_chat

    def load_state(self, state_location: str | Path):
        try:
            self.chat_session.load_state(state_location)
            for chat_message in self.chat_session.messages:
                self.chat_window.message_recived.emit(
                    chat_message.model_dump()
                )

            logger.info('loaded previous state')
        except FileNotFoundError as e:
            logger.info(
                'No previous state found at persistence location, skipped loading state'
            )

    def save_state(self, state_location: str | Path):
        self.chat_session.save_state(state_location)
        logger.info('Saved curent state')

    def send_message(self, message: ChatMessage):
        self.chat_session.add_message(message)
        self.chat_window.message_recived.emit(message.model_dump())

    def clear_chat_session(self):
        self.chat_session.clear_state()
        if self.on_clear_chat is not None:
            self.on_clear_chat()
        logger.info('Cleared curent state')

    def process_user_message(self, message: ChatMessage):
        self.send_message(message)
        if self.on_user_message is not None:
            self.on_user_message(message.content)

    def process_assistant_message(self, message: ChatMessage):
        self.send_message(message)
        if self.on_assistant_message is not None:
            self.on_assistant_message()

    def open_settings(self):
        content_future = self._pool.submit(
            texteditor.open, filename=self.settings_location
        )

        def write_content_update(content: Future[str]):
            content = content.result()
            with self.settings_location.open('w') as settings_file:
                settings_file.write(content)

        content_future.add_done_callback(write_content_update)

    def show(self):
        self.chat_window.show()
        self.chat_window.raise_()
        self.chat_window.activateWindow()
