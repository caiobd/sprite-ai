from __future__ import annotations

import sys
import threading as th

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from pet.sprite_sheet.animation import Animation, AnimationController
from pet.sprite_sheet.movement import LinearMovement, Movement
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from pet.sprite_widget import SpriteWidgetQt


class Pet:
    def __init__(
        self,
        sprite_sheet_metadata: SpriteSheetMetadata,
        animations: dict[str, Animation],
        movements: dict[str, Movement],
    ):
        self._app = QtWidgets.QApplication(sys.argv)
        self.sprite_widget = SpriteWidgetQt()
        self.movements = movements
        sprite_sheet_image = QPixmap(sprite_sheet_metadata.path)
        self.animation_controller = AnimationController(
            sprite_sheet_image, sprite_sheet_metadata, animations
        )
        self.image_update_rate: float | int = 0.1
        self.position_update_rate: float | int = 0.2
        self._image_update_timer: th.Timer = None
        self._position_update_timer: th.Timer = None
        self._movement: Movement = None

    def _update_image_loop(self):
        self._image_update_timer = th.Timer(
            self.image_update_rate, self._update_image_loop
        )
        self._image_update_timer.start()
        self.sprite_widget.image = self.animation_controller.frame

    def _update_position_loop(self):
        self._position_update_timer = th.Timer(
            self.position_update_rate, self._update_position_loop
        )
        self._position_update_timer.start()
        if self._movement is not None:
            self._movement.step()
            self.sprite_widget.position = self._movement.position

    def event_loop(self):
        self.sprite_widget.show()
        self._update_image_loop()
        self._update_position_loop()
        self.animation_controller.set_animation("walking_left")
        self.animation_controller.play()
        self.sprite_widget.position = (500, 500)
        self._app.exec()

    def set_movement(self, name: str):
        try:
            self._movement = self.movements[name]
        except KeyError:
            raise ValueError(f"Invalid movement: {name}")

    def set_animation(self, name: str):
        self.animation_controller.set_animation(name)


def main():
    animations = {
        "idle": Animation(0, 0, 0.2),
        "walking_left": Animation(0, 3, 0.2, flip_x=True),
        "walking_right": Animation(0, 3, 0.2),
        "jumping": Animation(2, 4, 0.2),
    }
    movements = {
        "idle": None,
        "walking": LinearMovement.from_tuple(
            (0, 0), (1000, 0), 100, loop=True, loop_reverse=True
        ),
        "jumping": LinearMovement.from_tuple((0, 0), (0, 0.2), 500, loop=True),
    }

    sprite_sheet_metadata = SpriteSheetMetadata(
        "resources/sprites/fred.png", 5888, 128, 46, 1
    )
    pet = Pet(sprite_sheet_metadata, animations, movements)
    pet.set_movement("walking")
    # pet.set_animation("walking")
    pet.event_loop()


if __name__ == "__main__":
    main()
