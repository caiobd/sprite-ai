from __future__ import annotations

import pickle
from dataclasses import dataclass

import yaml
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate


@dataclass
class LanguageModel:
    model_name: str
    system_prompt: str = ""
    model_temperature: float = 0.7
    context_size: int = 4096
    llm_chain: LLMChain | None = None

    def _build_prompt_template(self) -> PromptTemplate:
        prompt_template = (
            "<|im_start|>system\n"
            "{system_prompt}<|im_end|>\n"
            "Chat History:\n"
            "{chat_history}\n"
            "<|im_start|>user\n"
            "{user_input}<|im_end|>\n"
            "<|im_start|>assistant\n"
        )

        prompt_template = prompt_template.format(
            system_prompt=self.system_prompt,
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
            model_path=self.model_name,
            n_ctx=self.context_size,
            # n_gpu_layers=40,
            temperature=self.model_temperature,
            echo=False,
            stop=["<|im_end|>"],
        )  # type: ignore
        memory = ConversationSummaryBufferMemory(
            llm=llm,
            memory_key="chat_history",
            human_prefix="user",
            ai_prefix="assistant",
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
