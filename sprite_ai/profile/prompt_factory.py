from sprite_ai.profile.sprite_profile_config import SpriteProfileConfig
from sprite_ai.defaults.default_profiles import PROFILES


class PromptFactory:
    def build(self, profile_config: SpriteProfileConfig) -> str:
        system_prompt = profile_config.system_prompt

        if not system_prompt:
            profile = PROFILES[profile_config.name]
            system_prompt = profile.default_prompt

        return system_prompt
