from __future__ import annotations

import pickle
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import platformdirs
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from llama_cpp import suppress_stdout_stderr
from loguru import logger
from pydantic import BaseModel

from sprite_ai.constants import APP_NAME
from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.utils.download import download_file


@dataclass
class LanguageModel:
    model_config: LanguageModelConfig
    llm_chain: LLMChain | None = None

    def _build_prompt_template(self) -> PromptTemplate:
        prompt_template = self.model_config.prompt_template

        prompt_template = prompt_template.format(
            system_prompt=self.model_config.system_prompt,
            chat_history="{chat_history}",
            user_input="{user_input}",
        )
        logger.debug(prompt_template)

        prompt = PromptTemplate(
            input_variables=["chat_history", "user_input"], template=prompt_template
        )
        return prompt

    def __post_init__(self) -> None:
        if not Path(self.model_location).exists():
            self._download_model()

        with suppress_stdout_stderr():
            llm = LlamaCpp(
                model_path=self.model_location,
                n_ctx=self.model_config.context_size,
                # n_gpu_layers=40,
                temperature=self.model_config.model_temperature,
                echo=False,
                stop=self.model_config.stop_strings,
            )  # type: ignore

        Memory = self.model_config.memory_type.value
        memory = Memory(
            llm=llm,
            memory_key="chat_history",
            human_prefix=self.model_config.user_prefix,
            ai_prefix=self.model_config.ai_prefix,
            max_token_limit=self.model_config.memory_tokens_limit,
        )
        prompt_template = self._build_prompt_template()
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            memory=memory,
            verbose=False,
        )
        self.llm_chain = llm_chain

    def awnser(self, prompt: str):
        if self.llm_chain:
            awnser = self.llm_chain.predict(user_input=prompt)
        else:
            raise RuntimeError("Failed to load llm model")

        return awnser

    def messages(self):
        return self.llm_chain.memory.chat_memory.messages

    def load_memory(self, memory_file_location: str):
        with open(memory_file_location, "rb") as memory_file:
            with suppress_stdout_stderr():
                memory = pickle.load(memory_file)
        self.llm_chain.memory = memory

    def save_memory(self, memory_file_location: str):
        with open(memory_file_location, "wb") as memory_file:
            pickle.dump(self.llm_chain.memory, memory_file)

    @property
    def model_location(self):
        user_data_location = platformdirs.user_data_path(
            appname=APP_NAME,
            appauthor=None,
            version=None,
            roaming=False,
            ensure_exists=True,
        )
        user_models_location = user_data_location / "models"
        user_models_location.mkdir(exist_ok=True)

        model_location = user_models_location / self.model_config.name
        model_location = str(model_location)
        return model_location

    def _download_model(self):
        download_file(self.model_config.url, self.model_location)
