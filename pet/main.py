from __future__ import annotations

from importlib import resources
import os
import threading as th

from plyer import notification
from plyer.utils import platform
import platformdirs

from pet.core.pet import Pet
from pet.core.pet_behaviour import PetBehaviour
from pet.core.world import World
from pet.default_animations import ANIMATIONS
from pet.default_states import POSSIBLE_STATES
from pet.gui.chat import ChatWindow
from pet.gui.pet_window import PetGui
from pet.language.language_model import LanguageModel
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from pet.language.default_model_configs import DOLPHIN_MINISTRAL_7B


APP_NAME = "Pet"
ICON_EXTENTION = icon_extension = "ico" if platform == "win" else "png"
ICON_FILE = str(resources.path("pet.resources.icons", f"icon.{ICON_EXTENTION}"))


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
    user_data_dir = platformdirs.user_data_path(
        appname=APP_NAME,
        appauthor=None,
        version=None,
        roaming=False,
        ensure_exists=True,
    )
    persistence_location = str(user_data_dir / "state")
    sprite_sheet_location = str(resources.path("pet.resources.sprites", "fred.png"))
    icon_location = str(resources.path("pet.resources.icons", "carboardbox_open.png"))
    print(sprite_sheet_location)
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
        print(f"Failed to load state, {e}")

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
        print("exiting...")
        os._exit(0)


if __name__ == "__main__":
    main()
