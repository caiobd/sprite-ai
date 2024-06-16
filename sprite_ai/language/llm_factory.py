from langchain.chat_models.base import BaseChatModel
from langchain_community.chat_models.ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether


class LLMFactory:
    def build(
        self,
        model_name: str,
        model_backend: str,
        context_size: int,
        temperature: float = 0.7,
        url: str = '',
        api_key: str = '',
    ) -> BaseChatModel:
        if model_backend == 'ollama':
            url = url if url else 'http://localhost:11434'
            llm = ChatOllama(
                model=model_name,
                num_ctx=context_size,
                temperature=temperature,
                base_url=url,
            )
        elif model_backend == 'openai':
            url = url if url else None
            llm = ChatOpenAI(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                openai_api_key=api_key,
                openai_api_base=url,
            )
        elif model_backend == 'together':
            url = url if url else 'https://api.together.xyz/inference'
            llm = ChatTogether(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                together_api_key=api_key,
                base_url=url,
            )
        elif model_backend == 'llamacpp':
            url = url if url else 'http://localhost:8000/v1'
            llm = ChatOpenAI(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                openai_api_key=api_key,
                openai_api_base=url,
            )
        elif model_backend == 'groq':
            url = url if url else None
            llm = ChatGroq(
                model=model_name,
                max_tokens=context_size,
                temperature=temperature,
                api_key=api_key,
                base_url=url,
            )
        else:
            raise ValueError('Unsuported model type')

        return llm
