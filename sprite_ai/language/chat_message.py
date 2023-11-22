from pydantic import BaseModel


class ChatMessage(BaseModel):
    sender: str
    content: str

    def __str__(self) -> str:
        return f"{self.sender}: {self.content}"
