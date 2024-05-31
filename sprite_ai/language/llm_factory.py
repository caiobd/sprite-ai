from langchain.chat_models.base import BaseChatModel
from langchain_community.chat_models.ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether


class LLMFactory:
    def build(
        self,
        model_name: str,
        context_size: int,
        temperature: float = 0.7,
        url: str = '',
        api_key: str = '',
    ) -> BaseChatModel:

        try:
            prefix_end_position = model_name.index('/')
        except ValueError as e:
            raise ValueError('Missing model backend in model name', e)
        model_name_start_position = prefix_end_position + 1
        model_prefix = model_name[:prefix_end_position]
        model_name = model_name[model_name_start_position:]

        if model_prefix == 'ollama':
            llm = ChatOllama(
                model=model_name,
                num_ctx=context_size,
                temperature=temperature,
                base_url=url,
            )
        elif model_prefix == 'openai':
            url = url if url else None
            llm = ChatOpenAI(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                openai_api_key=api_key,
                openai_api_base=url,
            )
        elif model_prefix == 'together':
            url = url if url else 'https://api.together.xyz/inference'
            llm = ChatTogether(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                together_api_key=api_key,
                base_url=url,
            )
        elif model_prefix == 'llamacpp':
            url = url if url else 'localhost:8000'
            llm = ChatOpenAI(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                openai_api_key=api_key,
                openai_api_base=url,
            )
        else:
            raise ValueError('Unsuported model type')

        return llm
