from __future__ import annotations

import pickle
from dataclasses import dataclass
from pydantic import BaseModel

from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from pet.language.default_model_configs import DOLPHIN_MINISTRAL_7B


@dataclass
class LanguageModel:
    llm_chain: LLMChain | None = None
    model_config = DOLPHIN_MINISTRAL_7B

    def _build_prompt_template(self) -> PromptTemplate:
        prompt_template = self.model_config.prompt_template

        prompt_template = prompt_template.format(
            system_prompt=self.model_config.system_prompt,
            chat_history="{chat_history}",
            user_input="{user_input}",
        )
        print(prompt_template)

        prompt = PromptTemplate(
            input_variables=["chat_history", "user_input"], template=prompt_template
        )
        return prompt

    def __post_init__(self) -> None:
        llm = LlamaCpp(
            model_path=self.model_config.model_name,
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
            memory = pickle.load(memory_file)
        self.llm_chain.memory = memory

    def save_memory(self, memory_file_location: str):
        with open(memory_file_location, "wb") as memory_file:
            pickle.dump(self.llm_chain.memory, memory_file)
