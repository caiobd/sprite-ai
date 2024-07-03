from __future__ import annotations

from pydantic import BaseModel

from sprite_ai.assistant.language_config import LanguageConfig
from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.profile.sprite_profile_config import SpriteProfileConfig


class AssistantConfig(BaseModel):
    language: LanguageConfig
    language_model: LanguageModelConfig
    profile: SpriteProfileConfig
