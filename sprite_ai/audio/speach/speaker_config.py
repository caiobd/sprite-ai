from __future__ import annotations

from typing import Literal
from pydantic import BaseModel


class SpeakerConfig(BaseModel):
    language: str
    voice_reference: str
    inference_device: Literal['auto', 'cpu', 'cuda'] = 'auto'
