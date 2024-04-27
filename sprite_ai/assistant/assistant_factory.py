from typing import Callable
from sprite_ai.assistant.assistant import Assistant
from sprite_ai.assistant.assistant_config import AssistantConfig
from sprite_ai.audio.speach.speaker_factory import SpeakerFactory
from sprite_ai.audio.transcriber import Transcriber
from sprite_ai.language.languaga_model_factory import LanguageModelFactory


class AssistantFactory:
    def build(
        self,
        assistant_config: AssistantConfig,
        on_transcription: Callable | None = None,
    ) -> Assistant:
        transcriber = Transcriber(device='cpu')
        language_model = LanguageModelFactory().build(
            assistant_config.language_model
        )
        speaker = SpeakerFactory().build(assistant_config.speaker)
        assistant = Assistant(
            transcriber,
            language_model,
            speaker,
            on_transcription,
        )
        return assistant
