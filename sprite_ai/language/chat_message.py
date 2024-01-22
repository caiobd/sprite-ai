import time
from pydantic import BaseModel


class ChatMessage(BaseModel):
    sender: str
    content: str
    timestamp: float = time.time()

    def __str__(self) -> str:
        return f"{self.sender}: {self.content}"
