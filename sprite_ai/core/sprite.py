from pathlib import Path
from threading import Timer
from typing import Callable
from sprite_ai.core.sprite_behaviour import SpriteBehaviour
from sprite_ai.core.sprite_state import SpriteState

from sprite_ai.gui.sprite_gui import SpriteGui
from sprite_ai.movement.coordinate import Coordinate
from sprite_ai.movement.movement_factory import MovementFactory
from sprite_ai.sprite_sheet.animation import Animation
from sprite_ai.sprite_sheet.sprite_sheet import SpriteSheetMetadata


class Sprite:
    def __init__(
        self,
        screen_size: tuple[int, int],
        sprite_sheet_metadata: SpriteSheetMetadata,
        animations: dict[str:Animation],
        states: dict[str:SpriteState],
        first_state: str,
        on_clicked: Callable,
        icon_location: str | Path = '',
    ) -> None:
        self.sprite_gui = self._build_gui(
            sprite_sheet_metadata,
            animations,
            screen_size,
            on_clicked,
            icon_location,
        )
        self.sprite_behaviour = SpriteBehaviour(
            possible_states=states, first_state=first_state
        )
        width, height = screen_size
        self.current_position = Coordinate(width // 2, height)
        self.movement_factory = MovementFactory(screen_size)
        self.change_state_timer: None | Timer = None
        self.animation = None
        self._update_state()

    def _build_gui(
        self,
        sprite_sheet_metadata: SpriteSheetMetadata,
        animations: dict[str:Animation],
        screen_size: tuple[int, int],
        on_clicked: Callable,
        icon_location: str | Path = '',
    ) -> SpriteGui:
        sprite_gui = SpriteGui(
            screen_size,
            sprite_sheet_metadata,
            animations,
            icon_location=icon_location,
            on_clicked=on_clicked,
            on_position_updated=self.on_position_update,
        )
        return sprite_gui

    def _update_state(self):
        state = self.sprite_behaviour.get_state()
        self.set_animation(state.animation)
        self.set_movement(state.movement)

    def next_state(self):
        self.sprite_behaviour.next_state()
        self._update_state()

    def state_change_loop(self):
        self.next_state()
        self.change_state_timer = Timer(5, self.state_change_loop)
        self.change_state_timer.start()

    def set_state(self, state_name: str):
        self.sprite_behaviour.set_state(state_name)
        self._update_state()

    def get_state(self):
        return self.sprite_behaviour.get_state()

    def on_position_update(self, position_update: dict[str, Coordinate]):
        old_position = position_update['old_position']
        new_position = position_update['new_position']
        self.current_position = new_position

    def set_animation(self, animation: str):
        self.animation = animation
        self.sprite_gui.set_animation(animation)

    def set_movement(self, movement_name: str):
        movement = self.movement_factory.build(
            movement_name, self.current_position
        )

        if self.animation is not None:
            self.sprite_gui.set_animation(self.animation)

        self.sprite_gui.set_movement(movement)

    def run(self):
        self.state_change_loop()
        self.sprite_gui.run()

    def shutdown(self):
        self.sprite_gui.shutdown()
