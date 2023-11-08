import time
from dataclasses import dataclass
from typing import Callable

import pyperclip
import yaml
from plyer import notification
from plyer.utils import platform
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
    def __init__(self, language_model: LanguageModel|None, chat_state: ChatState|None=None) -> None:
        if chat_state is None:
            chat_state = ChatState()
        self.chat_state = chat_state
        self.commands = [
            Command('+ new message', self._new_message_menu)
        ]
        self.language_model = language_model
        self._rofi = Rofi()
    
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
        awnser = self.language_model.awnser(chat_message.content)
        notification.notify(
            title='Pet',
            message=awnser,
            app_name='Pet',
            # app_icon='path/to/the/icon.{}'.format(
            #     # On Windows, app_icon has to be a path to a file in .ICO format.
            #     'ico' if platform == 'win' else 'png'
            # )
        )
        chat_message_awnser = ChatMessage(sender='😸 | cat', content=awnser)
        self.chat_state.chat_history.append(chat_message_awnser)
        self._main_menu()

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

def main():
    STATE_FILE = 'chat_state.yml'
    MODEL_FILE = 'model.pickle'

    model_name = '/home/red/repos/pet/pet_qt/llama-2-7b-chat.Q4_0.gguf'
    system_prompt = (
        'You are a helpful AI assistant, you always only answer for the assistant then you stop.\n'
        'You always awnser in Brazilian Portuguese. read the chat history to get context.\n'
        'Notice that the AI wont translate its awnser to another laguage, it will only awnser in Brazilian Portuguese.\n'
        'You are a portuguese speaking cat ai, so you speak like a cat'
        'Example:\n'
        'Human: Oi tudo bem?\n'
        'AI: Olá, como posso ajuda-lo?\n'
        'Human: Quer peixe?\n'
        'AI: Miau!!! Amo peixe? É meaw favorito!\n'
        'Human: Qual seu nome?\n'
        'AI: Eu sou sou Gato o gato assistente\n'
    )
    try:
        language_model = LanguageModel.from_file(MODEL_FILE)
    except FileNotFoundError as e:
        language_model = LanguageModel(
            model_name,
            system_prompt
        )
    
    try:
        chat_state = ChatState.from_file(STATE_FILE)
    except FileNotFoundError as e:
        chat_state = ChatState()

    chat_window = ChatWindow(language_model, chat_state)
    chat_window.show()
    chat_state.to_file(STATE_FILE)
    language_model.to_file(MODEL_FILE)

if __name__ == "__main__":
    main()
