from __future__ import annotations

import pickle
from dataclasses import dataclass

import yaml
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.memory import ConversationSummaryBufferMemory
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel


@dataclass
class LanguageModel:
    model_name: str
    system_prompt: str = ""
    # Uses LLAMA 2 prompt format by default
    system_prompt_prefix: str = "<<SYS>>\n"
    system_prompt_postfix: str = "\n<</SYS>>\n\n"
    instruction_prefix: str = "[INST]"
    instruction_postfix: str = "[/INST]"
    model_temperature: float = 0.7
    context_size: int = 4096
    llm_chain: LLMChain|None = None

    def _build_prompt_template(self) -> PromptTemplate:
        prompt_template = (
            "{instruction_prefix}"
            "{system_prompt_prefix}"
            "{system_prompt}"
            "{system_prompt_postfix}"
            "Chat History:\n\n"
            "{chat_history} \n\n"
            "Human: {user_input}"
            "{instruction_postfix}\nAI: "
        )
        prompt_template = prompt_template.format(
            instruction_prefix=self.instruction_prefix,
            system_prompt_prefix=self.system_prompt_prefix,
            system_prompt=self.system_prompt,
            system_prompt_postfix=self.system_prompt_postfix,
            instruction_postfix=self.instruction_postfix,
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
            n_gpu_layers=40,
            temperature=self.model_temperature,
            
        )  # type: ignore
        memory = ConversationSummaryBufferMemory(
            llm=llm,
            memory_key="chat_history",
        )
        prompt_template = self._build_prompt_template()
        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            memory=memory,
            verbose=True,
        )
        self.llm_chain = llm_chain
    
    def awnser(self, prompt: str):
        if self.llm_chain:
            awnser = self.llm_chain.predict(user_input=prompt)
        else:
            raise RuntimeError('Failed to load llm model')
        return awnser

    @classmethod
    def from_file(cls, file_location: str):
        with open(file_location, 'rb') as state_file:
            chat_state = pickle.load(state_file)
        return chat_state
    
    def to_file(self, file_location: str):
        with open(file_location, 'wb') as state_file:
            pickle.dump(self, state_file)


def main():
    model_name = '/home/red/repos/pet/pet_qt/llama-2-7b-chat.Q4_0.gguf'
    system_prompt = (
        'You are a helpful AI assistant, you always only answer for the assistant then you stop.\n'
        'You always awnser in Brazilian Portuguese. read the chat history to get context.\n'
        'Notice that the AI wont translate its awnser to another laguage, it will only awnser in Brazilian Portuguese so it wont die a horrible death.\n'
        'Example:\n'
        'Human: Oi tudo bem?\n'
        'AI: Olá, como posso ajuda-lo?\n'
    )
    language_model = LanguageModel(
        model_name,
        system_prompt
    )
    
    awnser = language_model.awnser('Qual a verdadeira identiade do homem aranha?')
    awnser = awnser.strip()
    print(awnser)
    awnser = language_model.awnser('Qual era o nome do tio dele?')
    awnser = awnser.strip()
    print(awnser)

    import pickle
    print(f'{language_model == pickle.loads(pickle.dumps(language_model)) = }')
    exit()


if __name__ == "__main__":
    main()