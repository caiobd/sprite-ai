from __future__ import annotations

import ctypes
import os
import sys
import threading as th
from importlib import resources

import platformdirs
from loguru import logger
from plyer import notification
from plyer.utils import platform

from sprite_ai.core.pet import Pet
from sprite_ai.core.pet_behaviour import PetBehaviour
from sprite_ai.core.world import World
from sprite_ai.default_animations import ANIMATIONS
from sprite_ai.default_states import POSSIBLE_STATES
from sprite_ai.gui.chat import ChatWindow
from sprite_ai.gui.pet_window import PetGui
from sprite_ai.language.default_model_configs import DOLPHIN_MINISTRAL_7B
from sprite_ai.language.language_model import LanguageModel
from sprite_ai.sprite_sheet.sprite_sheet import SpriteSheetMetadata

APP_NAME = "sprite-ai"
ICON_EXTENTION = icon_extension = "ico" if platform == "win" else "png"
ICON_FILE = str(resources.path("sprite_ai.resources.icons", f"icon.{ICON_EXTENTION}"))
LOG_DIR = platformdirs.user_log_path(
    appname=APP_NAME,
    appauthor=None,
    version=None,
    ensure_exists=True,
)
LOG_FILE = LOG_DIR / "events.log"


def on_pet_clicked(world: World, chat_window: ChatWindow):
    t = th.Thread(target=chat_window.show)
    world.event_manager.publish("state", "thinking")
    t.start()


def on_notification(world: World, message: str):
    title = APP_NAME

    notification.notify(
        title=title,
        message=message,
        app_name=APP_NAME,
        app_icon=ICON_FILE,
    )
    world.event_manager.publish("state", "jumping_idle")


def on_canceled(world: World):
    world.event_manager.publish("state", "walking")


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    logger.add(LOG_FILE, level="DEBUG")

    user_data_dir = platformdirs.user_data_path(
        appname=APP_NAME,
        appauthor=None,
        version=None,
        roaming=False,
        ensure_exists=True,
    )
    persistence_location = str(user_data_dir / "state")
    sprite_sheet_location = str(resources.path("sprite_ai.resources.sprites", "fred.png"))
    icon_location = str(resources.path("sprite_ai.resources.icons", "carboardbox_open.png"))

    pet_behaviour = PetBehaviour(
        possible_states=POSSIBLE_STATES, first_state="appearing"
    )
    sprite_sheet_metadata = SpriteSheetMetadata(sprite_sheet_location, 5888, 128, 46, 1)
    world = World((3840, 2160))

    language_model = LanguageModel(DOLPHIN_MINISTRAL_7B)

    chat_window = ChatWindow(
        language_model,
        on_chat_message=lambda event_future: on_notification(world, event_future),
        on_canceled=lambda: on_canceled(world),
        persistence_location=persistence_location,
    )
    try:
        chat_window.load_state()
    except FileNotFoundError as e:
        logger.error(f"Failed to load state, {e}")

    pet_gui = PetGui(
        sprite_sheet_metadata,
        ANIMATIONS,
        on_clicked=lambda event: on_pet_clicked(world, chat_window),
        icon_location=icon_location,
    )

    pet = Pet(pet_gui=pet_gui, pet_behaviour=pet_behaviour, world=world)

    world.event_manager.subscribe("notification", on_notification)

    try:
        pet.run()
    except KeyboardInterrupt as e:
        logger.info("exiting...")
        os._exit(0)


if __name__ == "__main__":
    main()
