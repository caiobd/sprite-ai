import os
from llama_cpp import suppress_stdout_stderr
from loguru import logger
import platformdirs
from sprite_ai.constants import APP_NAME
from sprite_ai.language.language_model import LanguageModel
from sprite_ai.language.language_model_config import LanguageModelConfig
from langchain.llms.ollama import Ollama
from langchain.llms.llamacpp import LlamaCpp
from langchain.llms.base import LLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory, ConversationSummaryMemory

from sprite_ai.utils.download import download_file

class LanguageModelFactory:
    def _get_model_location(self, model_name: str) -> str:
        user_data_location = platformdirs.user_data_path(
            appname=APP_NAME,
            appauthor=None,
            version=None,
            roaming=False,
            ensure_exists=True,
        )
        user_models_location = user_data_location / "models"
        user_models_location.mkdir(exist_ok=True)

        model_location = user_models_location / model_name
        model_location = str(model_location)
        return model_location
    
    def _build_local_llm(self, model_config: LanguageModelConfig, model_name: str) -> LLM:
        model_location = self._get_model_location(model_name)
        if not os.path.isfile(model_location):
            download_file(model_config.url, model_location)
        with suppress_stdout_stderr():
            llm = LlamaCpp(
                model_path=model_location,
                n_ctx=model_config.context_size,
                # n_gpu_layers=40,
                temperature=model_config.model_temperature,
                echo=False,
                stop=model_config.stop_strings,
            )  # type: ignore
        return llm

    def _build_prompt_template(self, model_config: LanguageModelConfig) -> PromptTemplate:
        prompt_template = model_config.prompt_template
        prompt_template = prompt_template.format(
            system_prompt=model_config.system_prompt,
            chat_history="{chat_history}",
            user_input="{user_input}",
        )
        logger.debug(prompt_template)

        prompt = PromptTemplate(
            input_variables=["chat_history", "user_input"], template=prompt_template
        )
        return prompt
    
    def _build_memory(self, model_config: LanguageModelConfig, llm: LLM):        
        if model_config.memory_type == 'summary':
            Memory = ConversationSummaryMemory
        elif model_config.memory_type == 'summary_buffer':
            Memory = ConversationSummaryBufferMemory
        else:
            raise ValueError(f'Unsuported memory type: {model_config.memory_type}')

        memory = Memory(
            llm=llm,
            memory_key="chat_history",
            human_prefix=model_config.user_prefix,
            ai_prefix=model_config.ai_prefix,
            max_token_limit=model_config.memory_tokens_limit,
        )
        return memory
    
    def _build_llm(self, model_config: LanguageModelConfig):
        try:
            prefix_end_position =  model_config.name.index('/')
        except ValueError as e:
            raise ValueError('Missing model backend in model name', e)
        model_name_start_position = prefix_end_position + 1
        model_prefix = model_config.name[:prefix_end_position]
        model_name = model_config.name[model_name_start_position:]

        if model_prefix == 'ollama':
            llm = Ollama(
                model=model_name,
                base_url=model_config.url
            )
        elif model_prefix == 'local':
            llm = self._build_local_llm(model_config, model_name)
        else:
            raise ValueError('Unsuported model type')
        
        return llm
    
    def _build_llm_chain(self, model_config : LanguageModelConfig) -> LLMChain:
        llm = self._build_llm(model_config)
        prompt_template = self._build_prompt_template(model_config)
        memory = self._build_memory(model_config, llm)

        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            memory=memory,
            verbose=False,
        )
        return llm_chain
    
    def build(self, model_config : LanguageModelConfig) -> LanguageModel:
        llm_chain = self._build_llm_chain(model_config)
        language_model = LanguageModel(llm_chain)

        return language_model