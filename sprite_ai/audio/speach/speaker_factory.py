from sprite_ai.audio.speach.speaker import Speaker
from sprite_ai.audio.speach.speaker_config import SpeakerConfig


class SpeakerFactory:
    def build(self, speaker_config: SpeakerConfig) -> Speaker:
        return Speaker(**speaker_config.model_dump())
