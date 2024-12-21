from sprite_ai.audio.speach.speaker import Speaker
import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def speaker() -> Speaker:
    return Speaker('pt_BR-faber-medium')


def test_speaker_inference_raises_no_exception(
    mocker: MockerFixture, speaker: Speaker
) -> None:
    mocker.patch('sounddevice.play')
    speaker('Bom dia')


def test_speaker_inference_raises_no_exception_when_called_five_times(
    mocker: MockerFixture, speaker: Speaker
) -> None:
    import time

    mocker.patch('sounddevice.play')
    for _ in range(5):
        speaker('Bom dia')


def test_speaker_inference_raises_no_exception_when_called_with_emoji(
    mocker: MockerFixture, speaker: Speaker
) -> None:
    mocker.patch('sounddevice.play')
    speaker('Isso é um 🐛')
