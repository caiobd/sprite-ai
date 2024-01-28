import time

from faster_whisper import WhisperModel


def transcribe(file_location: str) -> str:
    model_size = 'small'
    model = WhisperModel(model_size, device='auto', compute_type='float16')

    start = time.time()
    segments, info = model.transcribe(
        file_location, beam_size=5, vad_filter=True
    )
    transcription_time = time.time() - start
    print(f'Tempo de transcrição: {transcription_time:.2f} segundos')

    print(
        "Detected language '%s' with probability %f"
        % (info.language, info.language_probability)
    )
    transcription = ''

    for segment in segments:
        transcription += segment.text

    return transcription
