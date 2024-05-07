from sprite_ai.assistant.language_config import LanguageConfig
from sprite_ai.audio.speach.speaker import Speaker


class SpeakerFactory:
    def build(self, language_config: LanguageConfig) -> Speaker:
        return Speaker(
            language_config.variant,
            language_config.speaker
        )
