from io import BytesIO
import time
from typing import Any

from faster_whisper import WhisperModel
from loguru import logger


class Transcriber:
    def __init__(self, model_size='small', device='auto') -> None:
        self.model_size = model_size
        self.model = WhisperModel(
            self.model_size, device=device, compute_type='float16'
        )

    def foward(self, audio: BytesIO | str, vad_filter=True) -> str:
        """Transcribes speach from audio

        Args:
            audio (BytesIO | str): Audio can be a file path or a ByteIO with audio content
            vad_filter (bool, optional): If True enables prefiltering with Voice Activity Detecion. Defaults to True.

        Returns:
            str: Audio transcription
        """
        start = time.time()
        segments, info = self.model.transcribe(
            audio, beam_size=5, vad_filter=vad_filter
        )

        logger.info(
            f'[Transcriber|PREDICTION] Language: {info.language}, Probability: { info.language_probability}'
        )
        transcription = ''

        for segment in segments:
            transcription += segment.text

        transcription_time = time.time() - start
        logger.info(
            f'[Transcriber|ELAPSED] Trascription {transcription_time:.2f}'
        )

        return transcription

    def __call__(self, audio: BytesIO | str, vad_filter=True) -> str:
        return self.foward(audio, vad_filter)
