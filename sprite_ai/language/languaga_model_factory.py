import os
from pathlib import Path

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from loguru import logger

from sprite_ai.language.language_model import LanguageModel
from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.language.llm_factory import LLMFactory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories.file import (
    FileChatMessageHistory,
)


class LanguageModelFactory:
    def _build_llm(self, model_config: LanguageModelConfig):
        llm_factory = LLMFactory()
        llm = llm_factory.build(
            model_config.name,
            model_config.backend,
            model_config.context_size,
            model_config.model_temperature,
            model_config.url,
            model_config.api_key,
        )

        return llm

    def _load_message_history(self, session_id: str) -> FileChatMessageHistory:
        return FileChatMessageHistory(f'{session_id}')

    def _build_llm_chain(
        self,
        model_config: LanguageModelConfig,
        persistency_location: str | Path,
    ) -> LLMChain:
        persistency_location = Path(persistency_location)

        def get_session_history(session_id: str) -> FileChatMessageHistory:
            session_location = (
                persistency_location / f'session_{session_id}.json'
            )
            return FileChatMessageHistory(session_location)

        prompt = ChatPromptTemplate.from_messages(
            [
                ('system', model_config.system_prompt),
                ('placeholder', '{chat_history}'),
                ('human', '{input}'),
            ]
        )
        llm = self._build_llm(model_config)

        with_message_history = RunnableWithMessageHistory(
            prompt | llm,
            get_session_history,
            input_messages_key='input',
            history_messages_key='chat_history',
        )

        return with_message_history

    def build(
        self,
        model_config: LanguageModelConfig,
        persistency_location: str | Path,
    ) -> LanguageModel:
        llm_chain = self._build_llm_chain(model_config, persistency_location)
        language_model = LanguageModel(llm_chain)

        return language_model
