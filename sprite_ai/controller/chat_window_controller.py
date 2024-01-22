from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from time import time

from loguru import logger
from sprite_ai.event_manager import EventManager
from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.chat_session import ChatSession
from sprite_ai.language.language_model import LanguageModel


class ChatWindowController:
    def __init__(self, event_manager: EventManager, language_model: LanguageModel, persistence_location:str) -> None:
        self.event_manager = event_manager
        self.language_model = language_model
        self.persistence_location = persistence_location
        
        self.chat_session = ChatSession(language_model)
        self._pool = ThreadPoolExecutor()
        self.event_manager.subscribe('process_user_message', self.process_user_message)

    def load_state(self):
        try:
            self.chat_session.load_state(self.persistence_location)
            for chat_message in self.chat_session.messages:
                self.event_manager.publish('ui.add_message', chat_message.model_dump())

            logger.info('loaded previous state')
        except FileNotFoundError as e:
            logger.info('No previous state found at persistence location, skipped loading state')
    
    def save_state(self):
        self.chat_session.save_state(self.persistence_location)
        logger.info('Saved curent state')

    def process_user_message(self, message: dict):
        content = message['content']
        timestamp = message['timestamp']
        self.chat_session.send_message(content, self._publish_awnser)

    def _publish_awnser(self, awnser_future: Future[str]):
        try:
            awnser = awnser_future.result()
        except CancelledError | TimeoutError as e:
            logger.error('Failed to aquire language model awnser', e)
            return
        
        message = {
            'sender': 'ai',
            'timestamp': time(),
            'content': awnser,
        }
        self.event_manager.publish('ui.add_message', message)
        self.save_state()
