import tempfile
from sprite_ai.audio.microphone import Microphone
from sprite_ai.audio.transcriber import Transcriber


class STT:
    def __init__(self) -> None:
        self.microphone = Microphone()
        self.transcriber = Transcriber()

    def listen(self, timeout=60) -> str:
        audio_file = tempfile.NamedTemporaryFile()
        silence_threshold = self.microphone.calibrate(0.2)
        self.microphone.record(
            audio_file.name,
            silence_threshold=silence_threshold,
            max_duration=timeout,
        )
        trascription = self.transcriber.transcribe(audio_file.name)
        audio_file.close()
        return trascription
