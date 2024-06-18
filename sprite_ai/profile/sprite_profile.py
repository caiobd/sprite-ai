from pydantic import BaseModel

from sprite_ai.sprite_sheet.animation import Animation


class SpriteProfile(BaseModel):
    name: str
    default_prompt: str
    sprite_sheet_rows: int
    sprite_sheet_columns: int
    animations: dict[str, Animation]
