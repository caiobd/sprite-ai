import time
import torch
from TTS.api import TTS
import sounddevice as sd
from loguru import logger


class Speaker:
    def __init__(
        self,
        language: str,
        voice_reference: str,
        inference_device: str = 'auto',
    ) -> None:
        # Get device
        if inference_device == 'auto':
            inference_device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.language = language
        self.voice_reference = voice_reference
        self.model: TTS = TTS(
            'tts_models/multilingual/multi-dataset/xtts_v2'
        ).to(inference_device)

    def foward(self, text: str):
        start = time.time()
        logger.info(f'[Speaker|PREDICTION]')
        audio = self.model.tts(
            text=text,
            speaker_wav=self.voice_reference,
            language=self.language,
        )
        elapsed_time = time.time() - start
        logger.info(
            f'[Speaker|ELAPSED] Speach generation time {elapsed_time:.2f}'
        )
        sd.play(audio, samplerate=22050)

    def __call__(self, text: str):
        self.foward(text)
