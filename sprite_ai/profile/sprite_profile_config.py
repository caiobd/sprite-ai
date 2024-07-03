from pydantic import BaseModel

# add name validation
class SpriteProfileConfig(BaseModel):
    name: str
    system_prompt: str | None = ''
