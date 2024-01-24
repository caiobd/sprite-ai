from __future__ import annotations

import os
import shutil
import sys
from importlib import resources

import platformdirs
import typer
import yaml
from loguru import logger
from plyer import notification
from plyer.utils import platform
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from sprite_ai.controller.chat_window_controller import ChatWindowController
from sprite_ai.core.sprite import Sprite
from sprite_ai.core.sprite_behaviour import SpriteBehaviour
from sprite_ai.core.world import World
from sprite_ai.default_animations import ANIMATIONS
from sprite_ai.default_states import POSSIBLE_STATES
from sprite_ai.gui.sprite_gui import SpriteGui
from sprite_ai.language.languaga_model_factory import LanguageModelFactory
from sprite_ai.language.language_model_config import LanguageModelConfig
from sprite_ai.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from sprite_ai.ui.chat_window import ChatWindow

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


def shutdown(app: QApplication):
    app.closeAllWindows()
    app.exit(0)
    os._exit(0)


def main():
    user_data_dir = platformdirs.user_data_path(
        appname=APP_NAME,
        appauthor=None,
        version=None,
        roaming=False,
        ensure_exists=True,
    )
    persistence_location = str(user_data_dir / 'state')
    sprite_sheet_location = str(
        resources.path('sprite_ai.resources.sprites', 'fred.png')
    )
    icon_location = str(
        resources.path('sprite_ai.resources.icons', 'carboardbox_open.png')
    )

    sprite_behaviour = SpriteBehaviour(
        possible_states=POSSIBLE_STATES, first_state='appearing'
    )
    sprite_sheet_metadata = SpriteSheetMetadata(
        sprite_sheet_location, 5888, 128, 46, 1
    )
    world = World((3840, 2160))

    config_location = user_data_dir / 'config.yaml'

    if not config_location.is_file():
        default_config_location = resources.path(
            'sprite_ai.resources', 'default_config.yaml'
        )
        shutil.copy2(default_config_location, config_location)

    with config_location.open(encoding='UTF-8') as config_file:
        model_config_dump = yaml.safe_load(config_file)
        model_config = LanguageModelConfig(**model_config_dump)

    language_model = LanguageModelFactory().build(model_config)

    app = QApplication(sys.argv)

    chat_window = ChatWindow(world.event_manager)
    chat_window_controller = ChatWindowController(
        world.event_manager, language_model, persistence_location
    )

    try:
        chat_window_controller.load_state()
    except FileNotFoundError as e:
        logger.error(f'Failed to load state, {e}')

    if icon_location:
        app.setWindowIcon(QIcon(icon_location))
    screen_size = app.primaryScreen().size()
    screen_size = (screen_size.width(), screen_size.height())

    sprite_gui = SpriteGui(
        screen_size,
        sprite_sheet_metadata,
        ANIMATIONS,
        on_clicked=lambda event: on_sprite_clicked(world, chat_window),
        icon_location=icon_location,
    )

    sprite = Sprite(
        sprite_gui=sprite_gui, sprite_behaviour=sprite_behaviour, world=world
    )

    world.event_manager.subscribe('notification', on_notification)
    world.event_manager.subscribe('exit', lambda _: shutdown(app))

    try:
        sprite.run()
        app.exec()
    except KeyboardInterrupt as e:
        logger.info('exiting...')
        os._exit(0)


if __name__ == '__main__':
    typer.run(main)
