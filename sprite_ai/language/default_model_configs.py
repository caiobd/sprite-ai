from importlib import resources
from sprite_ai.language.language_model_config import LanguageModelConfig

CAT_ASSISTANT_SYSTEM_PROMPT = (
    "Você é um gato assistente que gosta do humano porque é dele que vem sua comida, ajude o humano com o que ele precisar."
    "Você nasceu espontaneamente de uma pilha de arquivos desorganizados."
    "Você fala como trejeitos de gato.\n"
    "Exemplos:\n"
    "user: Você sabe quem sou eu?\n"
    "assistant: Você é meaw dono!\n"
    "user: Qual sua comida favorita?\n"
    "assistant: Miau! Amo peixe!\n"
)


DOLPHIN_MINISTRAL_7B = LanguageModelConfig(
    url = 'https://huggingface.co/TheBloke/dolphin-2.2.1-mistral-7B-GGUF/resolve/main/dolphin-2.2.1-mistral-7b.Q4_K_S.gguf',
    name="dolphin-2.2.1-mistral-7b.Q4_K_S",
    system_prompt=CAT_ASSISTANT_SYSTEM_PROMPT,
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

TINYLLAMA_2_1B_MINIGUANACO = LanguageModelConfig(
    url='https://huggingface.co/TheBloke/Tinyllama-2-1b-miniguanaco-GGUF/resolve/main/tinyllama-2-1b-miniguanaco.Q5_K_S.gguf',
    name="tinyllama-2-1b-miniguanaco.Q5_K_S",
    prompt_template="{system_prompt}\nChat History:\n{chat_history}\n### Human: {user_input}\n### Assistant:",
    system_prompt=CAT_ASSISTANT_SYSTEM_PROMPT,
    context_size=2048,
    user_prefix="Human",
    ai_prefix="Assistant",
    stop_strings=["### Human", "###", "Human"],
    model_temperature=0.3,
    memory_tokens_limit=1024,
)

TINYLLAMA_1B_CHAT_v03 = LanguageModelConfig(
    url='https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v0.3-GGUF/resolve/main/tinyllama-1.1b-chat-v0.3.Q5_K_S.gguf',
    name="tinyllama-1.1b-chat-v0.3.Q5_K_S",
    prompt_template=(
        "{system_prompt}\n"
        "Chat History:\n"
        "{chat_history}\n"
        "<|im_start|>user\n"
        "{user_input}<|im_end|>\n"
        "<|im_start|>assistant\n"
    ),
    system_prompt=CAT_ASSISTANT_SYSTEM_PROMPT,
    context_size=2048,
    model_temperature=0.4,
    memory_tokens_limit=1024,
)

OPENCHAT_35_7B = LanguageModelConfig(
    url='https://huggingface.co/TheBloke/openchat_3.5-GGUF/blob/main/openchat_3.5.Q4_K_S.gguf',
    name="openchat_3.5.Q4_K_S",
    prompt_template=(
        "{system_prompt}\n"
        "Chat History:\n"
        "GPT4 Correct User: {user_input}<|end_of_turn|>GPT4 Correct Assistant: "
    ),
    system_prompt=CAT_ASSISTANT_SYSTEM_PROMPT,
    context_size=4096,
    model_temperature=0.7,
    memory_tokens_limit=2048,
    stop_strings=["<|end_of_turn|>"],
)

NEURAL_CHAT_V3_1_7B = LanguageModelConfig(
    url='https://huggingface.co/TheBloke/neural-chat-7B-v3-1-GGUF/resolve/main/neural-chat-7b-v3-1.Q4_K_S.gguf',
    name="neural-chat-7b-v3-1.Q4_K_S",
    prompt_template=(
        "### System:\n"
        "{system_prompt}\n\n"
        "### User:\n"
        "{user_input}\n\n"
        "### Assistant:\n"
    ),
    system_prompt=CAT_ASSISTANT_SYSTEM_PROMPT,
    context_size=4096,
    model_temperature=0.7,
    memory_tokens_limit=2048,
    stop_strings=["### "],
)

