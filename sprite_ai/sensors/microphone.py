from io import BytesIO
import os
import time
import wave
from loguru import logger
import numpy as np
import pyaudio
from silero_vad import SileroVAD
from faster_whisper.utils import get_assets_path


def int2float(sound):
    abs_max = np.abs(sound).max()
    sound = sound.astype('float32')
    if abs_max > 0:
        sound *= 1 / 32768
    sound = sound.squeeze()
    return sound


class Microphone:
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self._pyaudio = pyaudio.PyAudio()
        vad_model_location = os.path.join(get_assets_path(), 'silero_vad.onnx')
        self.vad_model = SileroVAD(vad_model_location)

    def _predict_speach_probability(self, audio_chunk: bytes) -> float:
        audio_chunk = np.frombuffer(audio_chunk, dtype=np.int16)
        audio_chunk = int2float(audio_chunk)
        speeach_probability = self.vad_model(audio_chunk, self.rate).item()
        return speeach_probability

    def calibrate(
        self,
        interval_seconds: float,
        min_treshold: float = 0.1,
        max_threshold: float = 0.8,
    ) -> int:
        logger.info('[STARTED] calibrating microphone')

        stream = self._pyaudio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        calibration_started_time = time.time()
        ambient_noise_data = []
        elapsed_calibration_time = 0

        while interval_seconds > elapsed_calibration_time:
            data = stream.read(self.chunk)
            speach_probability = self._predict_speach_probability(data)

            ambient_noise_data.append(speach_probability)
            elapsed_calibration_time = time.time() - calibration_started_time

        stream.stop_stream()
        stream.close()

        # chooses a value between min_threshold and max_threshold to be the silence threshold
        silence_threshold = min(
            np.median(ambient_noise_data) + min_treshold, max_threshold
        )

        logger.info('[FINISHED] calibrating microphone')

        return silence_threshold

    def record(
        self,
        max_duration=60,
        max_silence_seconds=2,
        patience=20,
        silence_threshold=0.5,
    ) -> BytesIO:
        logger.info('[STARTED] Microfone recording')

        stream = self._pyaudio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        frames = []
        record_time = 0
        last_speach = time.time()
        consecutive_silece_windows = 0

        while record_time < max_duration:
            data = stream.read(self.chunk)
            speach_probability = self._predict_speach_probability(data)
            logger.debug(f'Speach probability: {speach_probability}')

            last_speach_time_delta = time.time() - last_speach

            if speach_probability > silence_threshold:
                last_speach = time.time()
                consecutive_silece_windows = 0
            else:
                consecutive_silece_windows += 1

                if consecutive_silece_windows > patience:
                    if last_speach_time_delta > max_silence_seconds:
                        break

            frames.append(data)
            record_time += len(data) / self.rate

        stream.stop_stream()
        stream.close()

        sample_size = self._pyaudio.get_sample_size(self.format)
        bytesio = BytesIO()
        wf = wave.open(bytesio, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(sample_size)
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        bytesio.seek(0)

        logger.info('[ENDED] Microfone recording')

        return bytesio
