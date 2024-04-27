from __future__ import annotations

from importlib import resources
from typing import Literal
from pydantic import BaseModel


class SpeakerConfig(BaseModel):
    language: str
    voice_reference: str = str(
        resources.path('sprite_ai.resources.voices', 'default.wav')
    )
    inference_device: Literal['auto', 'cpu', 'cuda'] = 'auto'
