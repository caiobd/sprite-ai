from pathlib import Path
import soundfile as sf
import sounddevice as sd


class Sound:
    def __init__(self, sound_location: str | Path):
        self.sound_location = sound_location
        self.audio_data, self.samplerate = sf.read(
            sound_location, always_2d=True
        )

    def play(self, blocking: bool = False):
        sd.play(self.audio_data, samplerate=self.samplerate, blocking=blocking)
