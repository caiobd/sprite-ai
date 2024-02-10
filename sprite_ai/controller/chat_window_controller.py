from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from pathlib import Path
from time import time
from typing import Callable

from loguru import logger
import texteditor

from sprite_ai.event_manager import EventManager
from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.chat_session import ChatSession
from sprite_ai.language.language_model import LanguageModel
from sprite_ai.ui.chat_window import ChatWindow


class ChatWindowController:
    def __init__(
        self,
        event_manager: EventManager,
        language_model: LanguageModel,
        persistence_location: str,
        settings_location: str | Path,
        on_exit: Callable,
        on_user_message: Callable,
    ) -> None:

        self.event_manager = event_manager
        self.chat_window = ChatWindow(
            on_clear_chat=self.clear_chat_session,
            on_user_message=self.process_user_message,
            on_open_settings=self.open_settings,
            on_exit=on_exit,
        )
        self.language_model = language_model
        self.persistence_location = persistence_location
        self.settings_location = Path(settings_location)

        self.chat_session = ChatSession(language_model)
        self._pool = ThreadPoolExecutor()
        self.on_user_message = on_user_message

    def load_state(self):
        try:
            self.chat_session.load_state(self.persistence_location)
            for chat_message in self.chat_session.messages:
                self.send_message(chat_message)

            logger.info('loaded previous state')
        except FileNotFoundError as e:
            logger.info(
                'No previous state found at persistence location, skipped loading state'
            )

    def send_message(self, message: ChatMessage):
        self.chat_window.message_recived.emit(message.model_dump())

    def save_state(self):
        self.chat_session.save_state(self.persistence_location)
        logger.info('Saved curent state')

    def clear_chat_session(self):
        self.chat_session.clear_state()
        logger.info('Cleared curent state')

    def process_user_message(self, message: dict):
        chat_message = ChatMessage(**message)

        self.send_message(chat_message)
        self.chat_session.send_message(
            chat_message.content, self._publish_awnser
        )
        self.on_user_message()

    def _publish_awnser(self, awnser_future: Future[str]):
        try:
            awnser = awnser_future.result()
        except CancelledError | TimeoutError as e:
            logger.error('Failed to aquire language model awnser', e)
            return
        finally:
            self.event_manager.publish('ui.sprite.state', 'jumping_idle')

        message = ChatMessage(sender='ai', content=awnser, timestamp=time())
        self.send_message(message)
        self.save_state()

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
