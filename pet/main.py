# from __future__ import annotations

import threading as th

from pet.core.pet import Pet
from pet.core.pet_behaviour import PetBehaviour
from pet.core.world import World
from pet.default_animations import ANIMATIONS
from pet.default_states import POSSIBLE_STATES
from pet.gui.chat import ChatState, ChatWindow
from pet.gui.pet_window import PetGui
from pet.language.language_model import LanguageModel
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata

STATE_FILE = 'chat_state.yml'
MODEL_FILE = 'model.pickle'




def load_language_model() -> LanguageModel:
    model_name = '/home/red/repos/pet/pet_qt/llama-2-7b-chat.Q4_0.gguf'
    system_prompt = (
        'You are a helpful AI assistant, you always only answer for the assistant then you stop.\n'
        'You always awnser in Brazilian Portuguese. read the chat history to get context.\n'
        'Notice that the AI wont translate its awnser to another laguage, it will only awnser in Brazilian Portuguese so it wont die a horrible death.\n'
        'Example:\n'
        'Human: Oi tudo bem?\n'
        'AI: Olá, como posso ajuda-lo?\n'
    )
    try:
        language_model = LanguageModel.from_file(MODEL_FILE)
    except FileNotFoundError as e:
        language_model = LanguageModel(
            model_name,
            system_prompt=system_prompt,
        )
    return language_model

def load_chat_state() -> ChatState:
    try:
        chat_state = ChatState.from_file(STATE_FILE)
    except FileNotFoundError as e:
        chat_state = ChatState()
    return chat_state

def on_pet_clicked(world: World, chat_window:ChatWindow):
    t = th.Thread(target=chat_window.show)
    world.event_manager.publish('animation', 'thinking')
    world.event_manager.publish('movement', 'idle')
    t.start()

def main():
    pet_behaviour = PetBehaviour(possible_states=POSSIBLE_STATES, first_state='idle')
    sprite_sheet_metadata = SpriteSheetMetadata("resources/sprites/fred.png", 5888, 128, 46, 1)
    world = World((3840,2160))

    language_model = load_language_model()
    chat_state = load_chat_state()

    chat_window = ChatWindow(language_model, chat_state)
    pet_gui = PetGui(sprite_sheet_metadata, ANIMATIONS, on_clicked=lambda event: on_pet_clicked(world, chat_window))
    
    pet = Pet(pet_gui=pet_gui, pet_behaviour=pet_behaviour, world=world)

    try:
        pet.run()
    except KeyboardInterrupt as e:
        print('exiting...')
        exit(0)

    # update_pet_position = partial(world.update_entity_position, "pet")
    # pet_gui.on_position_updated = update_pet_position

    # world.event_manager.subscribe("animation", pet_gui.set_animation)
    # world.event_manager.subscribe("movement", pet_gui.set_movement)
    # world.event_manager.subscribe("world_clock", world.change_movement_event)

    # pet_gui.gui_loop()
    # pet_gui._image_update_timer.cancel()
    # pet_gui._image_update_timer.join()
    # pet_gui._position_update_timer.cancel()
    # pet_gui._position_update_timer.join()


if __name__ == "__main__":
    main()
