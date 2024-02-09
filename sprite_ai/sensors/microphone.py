import audioop
import time
import wave
from loguru import logger
import pyaudio


class Microphone:
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self._pyaudio = pyaudio.PyAudio()

    def calibrate(self, interval_seconds: float) -> int:
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
            rms = audioop.rms(data, 2)
            ambient_noise_data.append(rms)
            elapsed_calibration_time = time.time() - calibration_started_time

        stream.stop_stream()
        stream.close()

        silence_threshold = max(ambient_noise_data)

        logger.info('[FINISHED] calibrating microphone')

        return silence_threshold

    def record(
        self,
        file_path,
        max_duration=60,
        max_silence_seconds=2,
        patience=20,
        silence_threshold=-1,
    ):
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
            frames.append(data)

            rms = audioop.rms(data, 2)
            last_speach_time_delta = time.time() - last_speach

            if rms > silence_threshold:
                state = 'listening'
                last_speach = time.time()
                consecutive_silece_windows = 0
            else:
                state = 'silence'
                consecutive_silece_windows += 1

                if consecutive_silece_windows > patience:
                    if last_speach_time_delta > max_silence_seconds:
                        break
            record_time += len(data) / self.rate

        stream.stop_stream()
        stream.close()

        sample_size = self._pyaudio.get_sample_size(self.format)
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(sample_size)
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        logger.info('[ENDED] Microfone recording')
