import yaml
from pydantic import BaseModel

from sprite_ai.language.chat_message import ChatMessage


class ChatState(BaseModel):
    chat_history: list[ChatMessage] = []

    @classmethod
    def from_file(cls, file_location: str):
        with open(file_location) as state_file:
            chat_state = yaml.safe_load(state_file)
        return cls(**chat_state)

    def to_file(self, file_location: str):
        with open(file_location, "w") as state_file:
            yaml.safe_dump(self.model_dump(), state_file)
