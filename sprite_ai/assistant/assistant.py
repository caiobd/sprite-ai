from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import time
from typing import Any, Callable

from loguru import logger
from sprite_ai.audio.speach.speaker import Speaker
from sprite_ai.audio.transcriber import Transcriber
from sprite_ai.language.language_model import LanguageModel


@dataclass
class Assistant:
    transcriber: Transcriber
    language_model: LanguageModel
    speaker: Speaker
    on_transcription: Callable | None = None

    def foward(self, user_request: BytesIO | str) -> str:
        """Processes user request

        Args:
            user_request (BytesIO | str): Can be an audio BytesIO or an input string,
            audios will be converted to text automatically.
        """
        if not isinstance(user_request, str) and not isinstance(
            user_request, BytesIO
        ):
            raise TypeError(
                f'Invalid type "{type(user_request)}", user_request must be BytesIO or str'
            )

        if isinstance(user_request, BytesIO):
            user_request = self.transcriber(user_request)
            self.on_transcription(user_request)

        logger.info('[STARTED] Language model inference')
        awnser_started = time.time()

        awnser = self.language_model(user_request)

        awnser_elapsed = time.time() - awnser_started
        logger.info('[FINISHED] Language model inference')
        logger.info(f'[LanguageModel | Elapsed Time] {awnser_elapsed}')

        logger.info('[STARTED] Speach generation')
        speach_generation_started = time.time()

        self.speaker(awnser)

        speach_generation_elapsed = time.time() - speach_generation_started
        logger.info('[FINISHED] Speach generation')
        logger.info(
            f'[SpeachGeneration | Elapsed Time] {speach_generation_elapsed}'
        )

        return awnser

    def save_state(self, save_location: str | Path):
        self.language_model.save_memory(save_location)

    def load_state(self, load_location: str | Path):
        self.language_model.load_memory(load_location)

    def __call__(self, user_request: BytesIO | str) -> str:
        return self.foward(user_request)
