from io import BytesIO
from typing import Any
from sprite_ai.audio.transcriber import Transcriber
from sprite_ai.language.languaga_model_factory import LanguageModelFactory
from sprite_ai.language.language_model import LanguageModel
from sprite_ai.language.language_model_config import LanguageModelConfig


class Assistant:
    def __init__(self, lm_config: LanguageModelConfig) -> None:
        self.transcriber = Transcriber()
        self.language_model = LanguageModelFactory().build(lm_config)

    def foward(self, user_request: BytesIO | str) -> str:
        """Processes user request

        Args:
            user_request (BytesIO | str): Can be an audio BytesIO or an input string,
            audios will be converted to text automatically.
        """
        if not isinstance(user_request, str) or not isinstance(
            user_request, BytesIO
        ):
            raise TypeError(
                f'Invalid type "{type(user_request)}", user_request must be BytesIO or str'
            )

        if isinstance(user_request, BytesIO):
            user_request = self.transcriber(user_request)

        awnser = self.language_model(user_request)

        return awnser

    def __call__(self, user_request: BytesIO | str) -> str:
        self.foward(user_request)
