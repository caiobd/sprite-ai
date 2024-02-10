from __future__ import annotations

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
from plyer import notification
from plyer.utils import platform
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from sprite_ai.assistant.assistant import Assistant

from sprite_ai.controller.chat_window_controller import ChatWindowController
from sprite_ai.core.sprite import Sprite
from sprite_ai.core.world import World
from sprite_ai.event_manager import EventManager
from sprite_ai.language.languaga_model_factory import LanguageModelFactory
from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.audio.stt import STT
from sprite_ai.ui.shortcut import ShortcutManager

APP_NAME = 'sprite-ai'
ICON_EXTENTION = icon_extension = 'ico' if platform == 'win' else 'png'
ICON_FILE = str(
    resources.path('sprite_ai.resources.icons', f'icon.{ICON_EXTENTION}')
)
LOG_DIR = platformdirs.user_log_path(
    appname=APP_NAME,
    appauthor=None,
    version=None,
    ensure_exists=True,
)
LOG_FILE = LOG_DIR / 'events.log'


def on_sprite_clicked(chat_window_controller: ChatWindowController):
    chat_window_controller.show()


def on_notification(world: World, message: str):
    title = APP_NAME

    notification.notify(
        title=title,
        message=message,
        app_name=APP_NAME,
        app_icon=ICON_FILE,
    )
    world.event_manager.publish('ui.sprite.state', 'jumping_idle')


def on_canceled(world: World):
    world.event_manager.publish('ui.sprite.state', 'walking')


def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level='DEBUG')
    logger.add(LOG_FILE, level='DEBUG')


def shutdown():
    os._exit(0)


def get_audio_prompt() -> str:
    stt = STT()
    transcription = stt.listen()
    return transcription


def toggle_audio_interaction(chat_window_controller: ChatWindowController):
    prompt = get_audio_prompt()
    message = {
        'sender': 'user',
        'timestamp': time.time(),
        'content': prompt,
    }
    chat_window_controller.process_user_message(message)


class App:
    def __init__(self, app_name: str):
        self.user_data_dir = platformdirs.user_data_path(
            appname=APP_NAME,
            appauthor=None,
            version=None,
            roaming=False,
            ensure_exists=True,
        )
        self.persistence_location = str(self.user_data_dir / 'state')
        self.sprite_sheet_location = str(
            resources.path('sprite_ai.resources.sprites', 'fred.png')
        )
        self.icon_location = str(
            resources.path('sprite_ai.resources.icons', 'carboardbox_open.png')
        )
        self.config_location = self.user_data_dir / 'config.yaml'
        lm_config = self.load_config(self.config_location)
        # self.assistant = Assistant(lm_config)
        self.language_model = LanguageModelFactory().build(
            lm_config
        )   # remove and use the assistant instead

        self.initialize_gui(self.config_location)
        self.initialize_sensors()

    def load_config(self, config_location: Path | str) -> LanguageModelConfig:
        config_location = Path(config_location)
        if not config_location.is_file():
            default_config_location = resources.path(
                'sprite_ai.resources', 'default_config.yaml'
            )
            shutil.copy2(default_config_location, config_location)

        with self.config_location.open(encoding='UTF-8') as config_file:
            model_config_dump = yaml.safe_load(config_file)
            model_config = LanguageModelConfig(**model_config_dump)

        return model_config

    def initialize_gui(self, config_location: Path | str):
        config_location = Path(config_location)
        self.world = World((3840, 2160))
        self.gui_backend = QApplication(sys.argv)
        self.chat_window_controller = ChatWindowController(  # this must be inserted in a frontend (ui) class along with all gui components
            self.world.event_manager,
            self.language_model,  # this must be removed from controller, this interface will be done via events
            self.persistence_location,
            config_location,
            on_exit=lambda: shutdown(),
        )
        try:
            self.chat_window_controller.load_state()
        except FileNotFoundError as e:
            logger.error(f'Failed to load state, {e}')

        if self.icon_location:
            self.gui_backend.setWindowIcon(QIcon(self.icon_location))
        screen_size = self.gui_backend.primaryScreen().size()
        screen_size = (screen_size.width(), screen_size.height())

        self.sprite = Sprite(
            world=self.world,
            sprite_sheet_location=self.sprite_sheet_location,
            on_clicked=lambda _: on_sprite_clicked(
                self.chat_window_controller
            ),
        )

    def initialize_sensors(self):
        shortcut_manager = ShortcutManager()
        shortcut_manager.register_shortcut(
            'Ctrl+Shift+A',
            lambda: toggle_audio_interaction(self.chat_window_controller),
        )
        self.world.event_manager.subscribe('notification', on_notification)

    def run(self):
        try:
            self.sprite.run()
            self.gui_backend.exec()
        except KeyboardInterrupt as e:
            logger.info('exiting...')
            os._exit(0)


def main():
    app = App(APP_NAME)
    app.run()


if __name__ == '__main__':
    typer.run(main)
