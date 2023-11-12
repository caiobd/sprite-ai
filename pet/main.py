# from __future__ import annotations

from concurrent.futures import Future
import os
import threading as th

from plyer import notification
from plyer.utils import platform

from pet.core.pet import Pet
from pet.core.pet_behaviour import PetBehaviour
from pet.core.world import World
from pet.default_animations import ANIMATIONS
from pet.default_states import POSSIBLE_STATES
from pet.gui.chat import ChatState, ChatWindow
from pet.gui.pet_window import PetGui
from pet.language.language_model import LanguageModel
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from importlib import resources

STATE_FILE = "chat_state.yml"
MODEL_FILE = "model.pickle"
APP_NAME = "Pet"
ICON_EXTENTION = icon_extension = "ico" if platform == "win" else "png"
ICON_FILE = str(resources.path("pet.resources.icons", f"icon.{ICON_EXTENTION}"))


def load_language_model() -> LanguageModel:
    model_location = str(
        resources.path(
            "pet.resources.model_weights", "dolphin-2.2.1-mistral-7b.Q4_K_S.gguf"
        )
    )

    system_prompt = (
        "Você é um gato assistente que gosta do humano porque é dele que vem sua comida, ajude o humano com o que ele precisar."
        "Você nasceu espontaneamente de uma pilha de arquivos desorganizados."
        "Você fala como trejeitos de gato.\n"
        "Exemplos:\n"
        "user: Você sabe quem sou eu?\n"
        "assistant: Você é meaw dono!\n"
        "user: Qual sua comida favorita?\n"
        "assistant: Miau! Amo peixe!\n"
    )
    try:
        language_model = LanguageModel.from_file(MODEL_FILE)
    except FileNotFoundError as e:
        language_model = LanguageModel(
            model_location,
            system_prompt=system_prompt,
        )
    return language_model


def load_chat_state() -> ChatState:
    try:
        chat_state = ChatState.from_file(STATE_FILE)
    except FileNotFoundError as e:
        chat_state = ChatState()
    return chat_state


def on_pet_clicked(world: World, chat_window: ChatWindow):
    t = th.Thread(target=chat_window.show)
    world.event_manager.publish("state", "thinking")
    t.start()


def on_notification(world: World, event_future: Future):
    message: str = event_future.result()
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
    sprite_sheet_location = str(resources.path("pet.resources.sprites", "fred.png"))
    print(sprite_sheet_location)
    pet_behaviour = PetBehaviour(
        possible_states=POSSIBLE_STATES, first_state="appearing"
    )
    sprite_sheet_metadata = SpriteSheetMetadata(sprite_sheet_location, 5888, 128, 46, 1)
    world = World((3840, 2160))

    language_model = load_language_model()
    chat_state = load_chat_state()

    chat_window = ChatWindow(
        language_model,
        chat_state,
        on_chat_message=lambda event_future: on_notification(world, event_future),
        on_canceled=lambda: on_canceled(world),
    )
    pet_gui = PetGui(
        sprite_sheet_metadata,
        ANIMATIONS,
        on_clicked=lambda event: on_pet_clicked(world, chat_window),
    )

    pet = Pet(pet_gui=pet_gui, pet_behaviour=pet_behaviour, world=world)

    world.event_manager.subscribe("notification", on_notification)

    try:
        pet.run()
    except KeyboardInterrupt as e:
        print("exiting...")
        os._exit(0)
    finally:
        print("saving model...")
        chat_window.language_model.to_file(MODEL_FILE)


if __name__ == "__main__":
    main()
