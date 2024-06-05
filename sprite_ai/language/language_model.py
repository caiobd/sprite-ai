from __future__ import annotations
from pathlib import Path

import pickle
from dataclasses import dataclass
from typing import Protocol

from langchain.chains import LLMChain
import yaml


class LanguageModel:
    def __init__(self, llm_chain: LLMChain):
        self.llm_chain = llm_chain

    def foward(self, prompt: str, session_id: str) -> str:
        if self.llm_chain:
            awnser = self.llm_chain.invoke(
                {'input': prompt},
                config={'configurable': {'session_id': session_id}},
            )
        else:
            raise RuntimeError('Failed to load llm model')

        return awnser.content

    def __call__(self, prompt: str, session_id: str) -> str:
        return self.foward(prompt, session_id)

    def messages(self, session_id: str):
        return self.llm_chain.get_session_history(session_id).messages

    def clear_memory(self, session_id: str):
        self.llm_chain.get_session_history(session_id).clear()
