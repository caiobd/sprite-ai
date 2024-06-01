from __future__ import annotations
from multiprocessing import Process
import time


import uvicorn

from llama_cpp.server.app import create_app
from llama_cpp.server.settings import Settings
from huggingface_hub import hf_hub_download


class LanguageModelServer:
    def __init__(
        self,
        hf_repo_id: str,
        file_name: str,
        host: str = 'localhost',
        port: int = 8000,
        context_size: int = 8192,
        cache: bool = True,
        model_alias: str | None = None,
        verbose: bool = False,
    ) -> None:
        self._server_process = Process(
            name='language_model_server',
            target=self._run,
            args=(
                hf_repo_id,
                file_name,
                host,
                port,
                context_size,
                cache,
                model_alias,
                verbose,
            ),
        )

    def start(self):
        self._server_process.start()

    def stop(self):
        self._server_process.terminate()
        self._server_process.join()
        self._server_process.close()

    @staticmethod
    def _run(
        hf_repo_id: str,
        file_name: str,
        host: str,
        port: int,
        context_size: int,
        cache: bool,
        model_alias: str | None,
        verbose: bool,
    ):
        model_location = hf_hub_download(
            repo_id=hf_repo_id,
            filename=file_name,
        )
        settings = Settings(
            model=model_location,
            model_alias=model_alias,
            n_ctx=context_size,
            host=host,
            port=port,
            cache=cache,
            verbose=verbose,
        )
        app = create_app(
            settings=settings,
        )
        uvicorn.run(app)


if __name__ == '__main__':
    server = LanguageModelServer(
        'cognitivecomputations/dolphin-2.9-llama3-8b-gguf',
        'dolphin-2.9-llama3-8b-q4_K_M.gguf',
    )
    server.start()
    time.sleep(10)
    server.stop()
