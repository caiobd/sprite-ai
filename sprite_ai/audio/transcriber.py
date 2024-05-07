from io import BytesIO
import time
from typing import Any, Literal

from faster_whisper import WhisperModel
from loguru import logger

ComputeDevice = Literal['cpu','cuda']|None
LanguageCode = str|None

class Transcriber:
    def __init__(self, model_size: str='small', language: LanguageCode = None, device: ComputeDevice=None) -> None:
        if device is None:
            device = 'auto'
        
        self.model_size = model_size
        self.model = WhisperModel(
            self.model_size, device=device, compute_type='default'
        )
        self.language = language

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
            audio, 
            language=self.language,
            beam_size=5, 
            vad_filter=vad_filter
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
