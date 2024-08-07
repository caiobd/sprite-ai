from pathlib import Path
from typing import Callable
from sprite_ai.assistant.assistant import Assistant
from sprite_ai.assistant.assistant_config import AssistantConfig
from sprite_ai.audio.speach.speaker_factory import SpeakerFactory
from sprite_ai.audio.transcriber import Transcriber
from sprite_ai.language.languaga_model_factory import LanguageModelFactory
from sprite_ai.profile.prompt_factory import PromptFactory
from sprite_ai.utils.locations import user_voices_location


class AssistantFactory:
    def build(
        self,
        assistant_config: AssistantConfig,
        persistency_location: str | Path,
        on_transcription: Callable | None = None,
    ) -> Assistant:
        language_code = assistant_config.language.language_code
        transcriber = Transcriber(language=language_code, device='cpu')
        system_prompt = PromptFactory().build(assistant_config.profile)
        language_model = LanguageModelFactory().build(
            assistant_config.language_model,
            persistency_location,
            system_prompt,
        )
        speaker = SpeakerFactory().build(
            assistant_config.language, user_voices_location
        )
        assistant = Assistant(
            transcriber,
            language_model,
            speaker,
            on_transcription,
        )
        return assistant
