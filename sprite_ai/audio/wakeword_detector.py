from importlib import resources
from pathlib import Path
from threading import Event
import openwakeword
from openwakeword.model import Model
import openwakeword.utils
import time
from loguru import logger
import pyaudio
import numpy as np
from threading import Event

from sprite_ai.audio.sound import Sound


class WakewordDetector:
    def __init__(
        self,
        model_location: str | Path,
        callback=None,
        detection_th: float = 0.5,
        cooldown_sec: float = 2,
    ):
        self.chunk = 1024
        self._format = pyaudio.paInt16
        self._channels = 1
        self._rate = 16000
        self._pyaudio = pyaudio.PyAudio()
        self._detection_active = Event()
        self.stream = None

        self._model_location = Path(model_location)
        self._model_backend = self._model_location.suffix[1:]
        self._wakeword = self._model_location.stem
        self.model = Model(
            wakeword_models=[model_location],
            inference_framework=self._model_backend,
        )
        self.detection_th = detection_th
        self.cooldown_sec = cooldown_sec

        self._callback = callback

    def _process_frame(
        self, audio_frame: bytes, chunk_size: int, time_info: dict, status: int
    ):
        audio_frame: np.ndarray = np.frombuffer(audio_frame, dtype=np.int16)

        if self._detection_active.is_set():
            prediction = self.model.predict(
                audio_frame,
                threshold={self._wakeword: self.detection_th},
                debounce_time=self.cooldown_sec,
            )
            prediction = tuple(prediction.values())
            predicted_confidence = prediction[0]

            if predicted_confidence > self.detection_th:
                if not self._callback is None:
                    self._callback()

        return (audio_frame, pyaudio.paContinue)

    def download_models(self):
        openwakeword.utils.download_models()

    def start(self):
        logger.info('[STARTED] Listening for wakeword')
        if self.stream is None:
            self.stream = self._pyaudio.open(
                format=self._format,
                channels=self._channels,
                rate=self._rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=self._process_frame,
                start=True,
            )
        self._detection_active.set()
        

    def stop(self):
        self._detection_active.clear()
        logger.info('[ENDED] Listening for wakeword')
    
    def shutdown(self):
        self._detection_active.clear()
        self.stream.stop_stream()
        self.stream.close()


if __name__ == '__main__':
    wakeword_alert_location = str(
        resources.path('sprite_ai.resources.sounds', 'listening_alert_01.wav')
    )
    wakeword_model_location = str(
        resources.path('sprite_ai.resources.wakewords', 'sprite.onnx')
    )
    alert = Sound(wakeword_alert_location)
    mic = WakewordDetector(wakeword_model_location, alert.play)
    mic.start()
    while True:
        try:
            time.sleep(1)
            logger.info('foreground')
        except KeyboardInterrupt:
            break
    mic.stop()
