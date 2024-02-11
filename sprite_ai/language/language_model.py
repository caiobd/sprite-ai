from __future__ import annotations
from pathlib import Path

import pickle
from dataclasses import dataclass
from typing import Protocol

from langchain.chains import LLMChain


class LanguageModel:
    def __init__(self, llm_chain: LLMChain):
        self.llm_chain = llm_chain

    def foward(self, prompt: str) -> str:
        if self.llm_chain:
            awnser = self.llm_chain.predict(user_input=prompt)
        else:
            raise RuntimeError('Failed to load llm model')

        return awnser

    def __call__(self, prompt: str) -> str:
        return self.foward(prompt)

    def messages(self):
        return self.llm_chain.memory.chat_memory.messages

    def load_memory(self, memory_file_location: str | Path):
        memory_file_location = Path(memory_file_location)
        with memory_file_location.open('rb') as memory_file:
            memory = pickle.load(memory_file)
        self.llm_chain.memory = memory

    def save_memory(self, memory_file_location: str | Path):
        memory_file_location = Path(memory_file_location)
        with memory_file_location.open('wb') as memory_file:
            pickle.dump(self.llm_chain.memory, memory_file)

    def clear_memory(self):
        self.llm_chain.memory.clear()
