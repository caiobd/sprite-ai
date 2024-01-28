import audioop
import time
import wave
import pyaudio


def record(
    file_path,
    duracao_maxima=20,
    silence_th=3000,
    max_silence_seconds=2,
    patience=5,
):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print('Gravação iniciada. Fale agora.')

    frames = []
    tempo_gravacao = 0
    last_speach = time.time()
    consecutive_silece_windows = 0

    while tempo_gravacao < duracao_maxima:
        data = stream.read(CHUNK)
        frames.append(data)

        rms = audioop.rms(data, 2)

        if rms > silence_th:
            state = 'listening'
            last_speach = time.time()
        else:
            state = 'silence'
            consecutive_silece_windows += 1

            if consecutive_silece_windows > patience:
                last_speach_time_delta = time.time() - last_speach
                if last_speach_time_delta > max_silence_seconds:
                    break

        print(f'{state = } rms = {rms:6.0f} {consecutive_silece_windows = }')
        tempo_gravacao += len(data) / RATE

    print('Gravação concluída. Salvando o arquivo...')

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
