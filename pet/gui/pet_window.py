

import sys
import threading
from typing import Any, Callable

import numpy as np
from pydantic import BaseModel
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from pet.movement import Movement
from pet.movement.coordinate import Coordinate
from pet.sprite_sheet.animation import Animation, AnimationController
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from pet.sprite_widget import SpriteWidgetQt


class PetGui:
    def __init__(
        self,
        sprite_sheet_metadata: SpriteSheetMetadata,
        animations: dict[str, Animation],
        on_position_updated: Callable | None = None,
        on_clicked: Callable|None = None,
    ):
        self._app = QtWidgets.QApplication(sys.argv)
        screen_size = self._app.primaryScreen().size()
        self.screen_size = (screen_size.width(), screen_size.height())
        self.sprite_widget = SpriteWidgetQt()
        sprite_sheet_image = QPixmap(sprite_sheet_metadata.path)
        self.animation_controller = AnimationController(
            sprite_sheet_image, sprite_sheet_metadata, animations
        )
        self.image_update_rate: float | int = 0.1
        self.position_update_rate: float | int = 0.2
        self._image_update_timer: threading.Timer | None = None
        self._position_update_timer: threading.Timer | None = None
        self._movement: Movement | None = None
        self.on_position_updated = on_position_updated
        if on_clicked is not None:
            self.sprite_widget.qwidget.mouseReleaseEvent=on_clicked

    def _update_image_loop(self):
        self._image_update_timer = threading.Timer(
            self.image_update_rate, self._update_image_loop
        )
        self._image_update_timer.start()
        self.sprite_widget.image = self.animation_controller.frame

    def _update_position_loop(self):
        self._position_update_timer = threading.Timer(
            self.position_update_rate, self._update_position_loop
        )
        self._position_update_timer.start()
        if self._movement is None:
            return

        x, y = self._movement.step()
        new_position = Coordinate(int(x), int(y))
        current_position = self.sprite_widget.position
        # has_position_changed = current_position != new_position
        self.sprite_widget.position = new_position

        if self.on_position_updated != None:
            position_update_message = {
                "old_position": current_position,
                "new_position": new_position,
            }
            self.on_position_updated(position_update_message)

    def gui_loop(self):
        width, height = self.screen_size
        self.sprite_widget.position = (width//2, height)
        self.sprite_widget.show()
        self._update_image_loop()
        self._update_position_loop()
        self.animation_controller.play()
        self._app.exec()

    def set_movement(self, movement: Movement):
        self._movement = movement

    def set_animation(self, name: str, flip_y: bool=False, flip_x: bool=False):
        self.animation_controller.set_animation(name, flip_y=flip_y, flip_x=flip_x)
    
    def run(self):
        try:
            self.gui_loop()
        finally:
            self._image_update_timer.cancel()
            self._image_update_timer.join()
            self._position_update_timer.cancel()
            self._position_update_timer.join()
