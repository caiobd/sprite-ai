from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from time import time

from loguru import logger
from sprite_ai.event_manager import EventManager
from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.chat_session import ChatSession
from sprite_ai.language.language_model import LanguageModel


class ChatWindowController:
    def __init__(self, event_manager: EventManager, language_model: LanguageModel, persistence_location: str = "") -> None:
        self.language_model = language_model
        self.chat_session = ChatSession(
            language_model, on_message=self._publish_awnser
        )
        self.persistence_location = persistence_location
        self.event_manager = event_manager
        self._pool = ThreadPoolExecutor()
        self.event_manager.subscribe('user_message', self.on_user_message)
    
    def on_user_message(self, message: dict):
        content = message['content']
        timestamp = message['timestamp']
        awnser_future = self._pool.submit(self.language_model.awnser, content)
        awnser_future.add_done_callback(self._publish_awnser)

    def _publish_awnser(self, awnser_future: Future[str]):
        try:
            awnser = awnser_future.result()
        except CancelledError | TimeoutError as e:
            logger.error('Failed to aquire language model awnser', e)
            return
        
        message = {
            'timestamp': time(),
            'content': awnser,
        }
        self.event_manager.publish('ai_message', message)
