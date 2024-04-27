from __future__ import annotations

from pydantic import BaseModel

from sprite_ai.audio.speach.speaker_config import SpeakerConfig
from sprite_ai.language.language_model_config import LanguageModelConfig


class AssistantConfig(BaseModel):
    language_model: LanguageModelConfig
    speaker: SpeakerConfig
