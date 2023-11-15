from importlib import resources
from pet.language.language_model_config import LanguageModelConfig


DOLPHIN_MINISTRAL_7B = LanguageModelConfig(
    model_name=str(
        resources.path(
            "pet.resources.model_weights", "dolphin-2.2.1-mistral-7b.Q4_K_S.gguf"
        )
    ),
    prompt_template=(
        "<|im_start|>system\n"
        "{system_prompt}<|im_end|>\n"
        "Chat History:\n"
        "{chat_history}\n"
        "<|im_start|>user\n"
        "{user_input}<|im_end|>\n"
        "<|im_start|>assistant\n"
    ),
)

