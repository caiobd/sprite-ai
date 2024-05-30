from pathlib import Path
import time
from typing import Literal
from urllib.error import URLError
import numpy as np
import onnxruntime
from piper.download import ensure_voice_exists, find_voice, get_voices
from piper.voice import PiperVoice
import sounddevice as sd
from loguru import logger

ComputeDevice = Literal['cpu', 'cuda'] | None


class Speaker:
    def __init__(
        self,
        variant: str,
        speaker_id: int = 0,
        inference_device: ComputeDevice = None,
        download_dir: str | Path = '.voices',
    ) -> None:
        if inference_device is None:
            inference_device = (
                'cuda' if onnxruntime.get_device() == 'GPU' else 'cpu'
            )
        use_cuda = inference_device == 'cuda'
        model_location, config_location = self._fetch_model(
            variant, download_dir
        )

        self.model: PiperVoice = PiperVoice.load(
            model_location, config_location, use_cuda
        )

        if self.model.config.num_speakers == 1:
            speaker_id = None
        self.speaker_id = speaker_id

    def _fetch_model(
        self, variant: str, download_dir: str | Path
    ) -> tuple[Path, Path]:
        Path(download_dir).mkdir(exist_ok=True)

        try:
            voices_info = get_voices(download_dir, update_voices=True)
        except URLError:
            voices_info = get_voices(download_dir)

        ensure_voice_exists(variant, [download_dir], download_dir, voices_info)
        model_location, config_location = find_voice(variant, [download_dir])

        return model_location, config_location

    def foward(self, text: str):
        start = time.time()
        logger.info(f'[Speaker|PREDICTION]')
        frames_stream = self.model.synthesize_stream_raw(text, self.speaker_id)
        elapsed_time = time.time() - start

        sample_rate = self.model.config.sample_rate
        first = True
        for frame in frames_stream:
            if first:
                logger.info(
                    f'[Speaker|ELAPSED] Time to first speach frame generation {elapsed_time:.2f}'
                )
                first = False

            frame = np.frombuffer(frame, dtype=np.int16)
            sd.play(frame, samplerate=sample_rate, blocking=True)

    def __call__(self, text: str):
        self.foward(text)
