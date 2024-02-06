import time

from faster_whisper import WhisperModel
from loguru import logger


class Transcriber:
    def __init__(self, model_size='small', device='auto') -> None:
        self.model_size = model_size
        self.model = WhisperModel(
            self.model_size, device=device, compute_type='float16'
        )

    def transcribe(self, file_location: str, vad_filter=True) -> str:
        start = time.time()
        segments, info = self.model.transcribe(
            file_location, beam_size=5, vad_filter=vad_filter
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
