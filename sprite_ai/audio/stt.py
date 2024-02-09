import tempfile
from sprite_ai.sensors.microphone import Microphone
from sprite_ai.audio.transcriber import Transcriber


class STT:
    def __init__(self) -> None:
        self.transcriber = Transcriber()
        self.microphone = Microphone()

    def listen(self, timeout=60) -> str:
        audio_file = tempfile.NamedTemporaryFile()
        silence_threshold = self.microphone.calibrate(0.5)
        self.microphone.record(
            audio_file.name,
            silence_threshold=silence_threshold,
            max_duration=timeout,
        )
        trascription = self.transcriber(audio_file.name)
        audio_file.close()
        return trascription
