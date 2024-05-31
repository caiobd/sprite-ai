from __future__ import annotations
from concurrent.futures import Future, ThreadPoolExecutor
from io import BytesIO

import os
from pathlib import Path
import shutil
import sys
from importlib import resources
import time

import platformdirs
import typer
import yaml
from loguru import logger

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from sprite_ai.assistant.assistant_config import AssistantConfig
from sprite_ai.assistant.assistant_factory import AssistantFactory

from sprite_ai.audio.sound import Sound
from sprite_ai.audio.wakeword_detector import WakewordDetector
from sprite_ai.controller.chat_window_controller import ChatWindowController
from sprite_ai.core.sprite import Sprite
from sprite_ai.language.chat_message import ChatMessage
from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.sensors.microphone import Microphone
from sprite_ai.ui.shortcut import ShortcutManager
from sprite_ai.constants import APP_NAME


class App:
    def __init__(self, app_name: str, log_level: str = 'INFO'):
        self.sprite_sheet_location = str(
            resources.path('sprite_ai.resources.sprites', 'fred.png')
        )
        self.icon_location = str(
            resources.path('sprite_ai.resources.icons', 'carboardbox_open.png')
        )

        self.listening_sound_location = str(
            resources.path(
                'sprite_ai.resources.sounds', 'listening_alert_01.wav'
            )
        )
        self.listening_sound = Sound(self.listening_sound_location)

        self.wakeword_model_location = str(
            resources.path('sprite_ai.resources.wakewords', 'sprite.onnx')
        )

        self.log_dir = platformdirs.user_log_path(
            appname=app_name,
            appauthor=None,
            version=None,
            ensure_exists=True,
        )
        self.user_data_dir = platformdirs.user_data_path(
            appname=app_name,
            appauthor=None,
            version=None,
            roaming=False,
            ensure_exists=True,
        )
        self.persistence_location = self.user_data_dir / 'state'
        self.config_location = self.user_data_dir / 'config.yaml'
        self.chat_state_location = self.persistence_location / 'state.yml'
        self.persistence_location.mkdir(parents=True, exist_ok=True)

        self.setup_logging(log_level)
        assistant_config = self.load_config(self.config_location)
        self.assistant = AssistantFactory().build(
            assistant_config,
            self.persistence_location,
            on_transcription=self.on_transcription,
        )
        self.initialize_gui(self.config_location)
        self.initialize_sensors()
        self._pool = ThreadPoolExecutor()

    def setup_logging(self, log_level='INFO'):
        log_location = self.log_dir / 'events.log'
        logger.remove()
        logger.add(sys.stdout, level=log_level)
        logger.add(log_location, level=log_level)

    def initialize_gui(self, config_location: Path | str):
        config_location = Path(config_location)
        self.gui_backend = QApplication(sys.argv)
        qscreen_size = self.gui_backend.primaryScreen().size()
        self.screen_size = (qscreen_size.width(), qscreen_size.height())
        self.chat_window_controller = ChatWindowController(  # this must be inserted in a frontend (ui) class along with all gui components
            config_location,
            on_exit=lambda: self.shutdown(),
            on_user_message=self.on_user_message,
            on_assistant_message=lambda: self.sprite.set_state('walking'),
            on_clear_chat=self.assistant.clear_state,
        )

        if self.icon_location:
            self.gui_backend.setWindowIcon(QIcon(self.icon_location))
        screen_size = self.gui_backend.primaryScreen().size()
        screen_size = (screen_size.width(), screen_size.height())

        self.sprite = Sprite(
            screen_size=self.screen_size,
            sprite_sheet_location=self.sprite_sheet_location,
            on_clicked=lambda _: self.on_sprite_clicked(),
        )

    def initialize_sensors(self):
        self.shortcut_manager = ShortcutManager()
        self.shortcut_manager.register_shortcut(
            'Ctrl+Shift+A',
            lambda: self.listen_prompt(),
        )
        self.microphone = Microphone()
        self.wakeword_detector = WakewordDetector(
            self.wakeword_model_location, self.listen_prompt
        )
        self.wakeword_detector.start()

    def load_config(self, config_location: Path | str) -> AssistantConfig:
        config_location = Path(config_location)
        if not config_location.is_file():
            default_config_location = resources.path(
                'sprite_ai.resources', 'default_config.yaml'
            )
            shutil.copy2(default_config_location, config_location)

        with self.config_location.open(encoding='UTF-8') as config_file:
            assistant_config_dump = yaml.safe_load(config_file)
            assistant_config = AssistantConfig.model_validate(
                assistant_config_dump
            )

        return assistant_config

    def save_state(self):
        self.chat_window_controller.save_state(self.chat_state_location)

    def load_state(self):
        self.chat_window_controller.load_state(self.chat_state_location)

    def prompt_assistant(self, prompt: str | BytesIO):
        assistant_response_future = self._pool.submit(self.assistant, prompt)

        def process_response(response_future: Future[str]):
            message = ChatMessage(
                sender='ai',
                content=response_future.result(),
                timestamp=time.time(),
            )
            self.chat_window_controller.process_assistant_message(message)

        def save_state(response_future: Future[str]):
            response_future.result()
            self.save_state()

        def listen_for_wakeword(response_future: Future[str]):
            self.wakeword_detector.start()

        assistant_response_future.add_done_callback(process_response)
        assistant_response_future.add_done_callback(save_state)
        assistant_response_future.add_done_callback(listen_for_wakeword)

    def on_user_message(self, prompt: str | BytesIO):
        self.sprite.set_state('thinking')
        self.prompt_assistant(prompt)

    def on_sprite_clicked(self):
        self.chat_window_controller.show()

    def on_transcription(self, transcription: str):
        message = ChatMessage(
            sender='user', content=transcription, timestamp=time.time()
        )
        self.chat_window_controller.send_message(message)

    def listen_prompt(self):
        self.wakeword_detector.stop()
        silence_threshold = self.microphone.calibrate(0.7)
        self.listening_sound.play(blocking=True)
        recording = self.microphone.record(silence_threshold=silence_threshold)
        self.on_user_message(recording)

    def run(self):
        try:
            self.load_state()
        except FileNotFoundError as e:
            logger.error(f'Failed to load state, {e}')

        try:
            self.sprite.run()
            self.gui_backend.exec()
        except KeyboardInterrupt as e:
            logger.info('exiting...')
            os._exit(0)
        finally:
            self.wakeword_detector.stop()
            self.wakeword_detector.shutdown()

    def shutdown(self):
        os._exit(0)


def main():
    app = App(APP_NAME, log_level='DEBUG')
    app.run()


if __name__ == '__main__':
    typer.run(main)
