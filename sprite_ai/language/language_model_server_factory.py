from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.language.language_model_server import LanguageModelServer


class LanguageModelServerFactory:
    def build(
        self, language_model_config: LanguageModelConfig
    ) -> LanguageModelServer | None:
        if language_model_config.backend != 'llamacpp':
            return None

        model_name = language_model_config.name
        try:
            if model_name.index(':') == len(model_name) - 1:
                raise ValueError('Missing model file name after ":"')
            if model_name.index(':') == 0:
                raise ValueError('Missing hugging face repo id before ":"')
        except ValueError as e:
            raise ValueError(
                'Missing hugging face repo id or model file name in language_model.name',
                e,
            )
        hf_repo_id, file_name = model_name.split(':')
        return LanguageModelServer(hf_repo_id, file_name)
