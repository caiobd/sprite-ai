from __future__ import annotations
from concurrent.futures import Future, ThreadPoolExecutor

import os
import shutil
import sys
from importlib import resources
import tempfile
import time
from typing import Callable

import platformdirs
import typer
import yaml
from loguru import logger
from plyer import notification
from plyer.utils import platform
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from sprite_ai.ui.shortcut import QtKeyBinder

from sprite_ai.controller.chat_window_controller import ChatWindowController
from sprite_ai.core.sprite import Sprite
from sprite_ai.core.sprite_behaviour import SpriteBehaviour
from sprite_ai.core.world import World
from sprite_ai.event_manager import EventManager
from sprite_ai.default_animations import ANIMATIONS
from sprite_ai.default_states import POSSIBLE_STATES
from sprite_ai.gui.sprite_gui import SpriteGui
from sprite_ai.language.languaga_model_factory import LanguageModelFactory
from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from sprite_ai.ui.chat_window import ChatWindow
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


def on_sprite_clicked(world: World, chat_window: ChatWindow):
    chat_window.show()
    chat_window.raise_()
    chat_window.activateWindow()


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


def shutdown(qapp: QApplication):
    os._exit(0)


def get_audio_prompt() -> str:
    stt = STT()
    transcription = stt.listen()
    return transcription


def toggle_audio_interaction(event_manager: EventManager):
    prompt = get_audio_prompt()
    message = {
        'sender': 'user',
        'timestamp': time.time(),
        'content': prompt,
    }
    event_manager.publish('ui.chat_window.add_message', message)
    event_manager.publish('ui.chat_window.process_user_message', message)


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

    def load_config(self) -> LanguageModelConfig:
        if not self.config_location.is_file():
            default_config_location = resources.path(
                'sprite_ai.resources', 'default_config.yaml'
            )
            shutil.copy2(default_config_location, self.config_location)

        with self.config_location.open(encoding='UTF-8') as config_file:
            model_config_dump = yaml.safe_load(config_file)
            model_config = LanguageModelConfig(**model_config_dump)

        return model_config


def main():
    app = App(APP_NAME)
    model_config = app.load_config()

    world = World((3840, 2160))

    language_model = LanguageModelFactory().build(model_config)

    qapp = QApplication(sys.argv)

    chat_window = ChatWindow(world.event_manager, app.config_location)
    chat_window_controller = ChatWindowController(
        world.event_manager, language_model, app.persistence_location
    )

    try:
        chat_window_controller.load_state()
    except FileNotFoundError as e:
        logger.error(f'Failed to load state, {e}')

    if app.icon_location:
        qapp.setWindowIcon(QIcon(app.icon_location))
    screen_size = qapp.primaryScreen().size()
    screen_size = (screen_size.width(), screen_size.height())

    sprite_sheet_metadata = SpriteSheetMetadata(
        app.sprite_sheet_location, 5888, 128, 46, 1
    )
    sprite_gui = SpriteGui(
        screen_size,
        sprite_sheet_metadata,
        ANIMATIONS,
        on_clicked=lambda event: on_sprite_clicked(world, chat_window),
        icon_location=app.icon_location,
    )

    sprite_behaviour = SpriteBehaviour(
        possible_states=POSSIBLE_STATES, first_state='appearing'
    )
    sprite = Sprite(
        sprite_gui=sprite_gui, sprite_behaviour=sprite_behaviour, world=world
    )
    shortcut_manager = ShortcutManager()
    shortcut_manager.register_shortcut(
        'Ctrl+Shift+A', lambda: toggle_audio_interaction(world.event_manager)
    )
    world.event_manager.subscribe('notification', on_notification)
    world.event_manager.subscribe('exit', lambda _: shutdown(app))

    try:
        sprite.run()
        qapp.exec()
    except KeyboardInterrupt as e:
        logger.info('exiting...')
        os._exit(0)


if __name__ == '__main__':
    typer.run(main)
