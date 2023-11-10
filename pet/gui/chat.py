from concurrent.futures import Future, ThreadPoolExecutor
from threading import Thread
import time
import sys
from dataclasses import dataclass
from typing import Callable

import pyperclip
import yaml
from pydantic import BaseModel
from rofi import Rofi

from pet.language.language_model import LanguageModel


class ChatMessage(BaseModel):
    sender: str
    content: str

    def __str__(self) -> str:
        return f'{self.sender}: {self.content}'

class ChatState(BaseModel):
    chat_history: list[ChatMessage] = []

    @classmethod
    def from_file(cls, file_location: str):
        with open(file_location) as state_file:
            chat_state = yaml.safe_load(state_file)
        return cls(**chat_state)
    
    def to_file(self, file_location: str):
        with open(file_location, 'w') as state_file:
            yaml.safe_dump(self.model_dump(), state_file)

@dataclass
class Command:
    name: str
    callback: Callable

    def __str__(self) -> str:
        return self.name

class ChatWindow:
    def __init__(self, language_model: LanguageModel|None, chat_state: ChatState|None=None, chat_message_callback: Callable|None = None) -> None:
        if chat_state is None:
            chat_state = ChatState()
        self.chat_state = chat_state

        # Implement command pattern here and inject commands via init
        # This allows for better extensibility and modularity
        self.commands = [
            Command('[x] exit', sys.exit),
            Command('+ new message', self._new_message_menu),
        ]
        self.language_model = language_model
        self._rofi = Rofi()
        self._pool = ThreadPoolExecutor()
        self._chat_message_callback = chat_message_callback
    
    def show(self):
        self._main_menu()

    @property
    def options(self):
        options = self.chat_state.chat_history + self.commands
        options.reverse()
        return options
    
    @property
    def options_names(self):
        options = [str(option) for option in self.options]
        return options

    def _new_message_menu(self):
        message = ''
        chat_history = self.chat_state.chat_history
        if chat_history:
            message = str(chat_history[-1])
        reponse = self._rofi.text_entry('👷 | you', message)
        chat_message = ChatMessage(sender='👷 | you', content=reponse)
        chat_history.append(chat_message)

        message_future = self._pool.submit(self.language_model.awnser, chat_message.content)

        message_future.add_done_callback(self._log_chat_awnser)
        if self._chat_message_callback is not None:
            message_future.add_done_callback(self._chat_message_callback)
    
    def _log_chat_awnser(self, message_future: Future):
        message: str = message_future.result()
        chat_message_awnser = ChatMessage(sender='😸 | cat', content=message)
        self.chat_state.chat_history.append(chat_message_awnser)

    def _main_menu(self):
        index, key = self._rofi.select('Option', self.options_names)
        
        if key == -1 or index == -1:
            return
        if index < len(self.commands):
            command = self.options[index]
            command.callback()
        else:
            selected_message = self.options[index]
            pyperclip.copy(selected_message.content)
