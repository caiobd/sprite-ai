from __future__ import annotations

import logging
import random
import sys
import threading as th
from ast import Call
from functools import partial
from multiprocessing import current_process
from time import time
from typing import Any, Callable, Sequence

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from pet import event_manager
from pet.movement import (
    BoomerangLoopMovement,
    ComposedMovement,
    Coordinate,
    LinearMovement,
    LoopMovement,
    Movement,
    SequenceMovement,
    coordinate,
)
from pet.sprite_sheet.animation import Animation, AnimationController
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from pet.sprite_widget import SpriteWidgetQt


class Pet:
    def __init__(
        self,
        sprite_sheet_metadata: SpriteSheetMetadata,
        animations: dict[str, Animation],
        on_position_updated: Callable | None = None,
    ):
        self._app = QtWidgets.QApplication(sys.argv)
        screen_size = self._app.primaryScreen().size()
        self.screen_size(screen_size.width(), screen_size.height())
        self.sprite_widget = SpriteWidgetQt()
        sprite_sheet_image = QPixmap(sprite_sheet_metadata.path)
        self.animation_controller = AnimationController(
            sprite_sheet_image, sprite_sheet_metadata, animations
        )
        self.image_update_rate: float | int = 0.1
        self.position_update_rate: float | int = 0.2
        self._image_update_timer: th.Timer | None = None
        self._position_update_timer: th.Timer | None = None
        self._movement: Movement | None = None
        self.on_position_updated = on_position_updated

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
        if self._movement is None:
            return

        x, y = self._movement.step()
        new_position = Coordinate(int(x), int(y))
        current_position = self.sprite_widget.position
        has_position_changed = current_position != new_position
        self.sprite_widget.position = new_position

        if self.on_position_updated != None:
            position_update_message = {
                "old_position": new_position,
                "new_position": new_position,
            }
            self.on_position_updated(position_update_message)

    def gui_loop(self):
        self.sprite_widget.show()
        self._update_image_loop()
        self._update_position_loop()
        self.animation_controller.play()
        self.sprite_widget.position = (500, 500)
        self._app.exec()

    def set_movement(self, movement: Movement):
        self._movement = movement

    def set_animation(self, name: str):
        self.animation_controller.set_animation(name)


def world_clock_loop():
    world_clock_timer = th.Timer(1, world_clock_loop)
    world_clock_timer.start()

    current_time = round(time())
    event_manager.publish("world_clock", current_time)


def change_animation_event(clock_time):
    if not isinstance(clock_time, int):
        raise TypeError("This event must receive integers")

    if clock_time % 2 == 0:
        animation = random.choice(
            ["idle", "walking_left", "walking_right", "jumping", "playing", "sliding"]
        )
        event_manager.publish("animation", animation)


def change_movement_event(clock_time):
    if clock_time % 5 == 0:
        
        target_x = random.choice(range(1000))
        target_y = random.choice(range(1000))
        start_coordinate = Coordinate(0, 0)
        target_coordinate = Coordinate(target_x, target_y)
        movement = LinearMovement(start_coordinate, target_coordinate, 20)
        event_manager.publish("movement", movement)


def event_loop():
    world_clock_loop()
    event_manager.subscribe("world_clock", change_animation_event)
    event_manager.subscribe("world_clock", change_movement_event)


class World:
    def __init__(self) -> None:
        self.entities: dict[str, Any] = {}
        self.event_manager = event_manager.EventManager()
        self.world_clock_timer = None
        self.world_clock_loop()

    def update_entity_position(self, entity_name, position_update_message):
        new_position = position_update_message["new_position"]
        old_position = position_update_message["old_position"]

        self.entities[entity_name] = position_update_message["new_position"]

        print(entity_name, new_position, old_position, flush=True)

    def world_clock_loop(self):
        self.world_clock_timer = th.Timer(1, world_clock_loop)
        self.world_clock_timer.start()

        current_time = round(time())
        event_manager.publish("world_clock", current_time)

    def change_movement_event(clock_time):
        if clock_time % 5 == 0:
            target_x = random.choice(range(1000))
            target_y = random.choice(range(1000))
            start_coordinate = Coordinate(
                random.choice(range(1000)), random.choice(range(1000))
            )
            target_coordinate = Coordinate(target_x, target_y)
            movement = LinearMovement(start_coordinate, target_coordinate, 20)
            event_manager.publish("movement", movement)


def main():
    animations = {
        "idle": Animation(0, 0, 0.2),
        "walking_left": Animation(0, 3, 0.2),
        "walking_right": Animation(0, 3, 0.2, flip_x=True, flip_y=False),
        "jumping": Animation(2, 4, 0.2),
        "playing": Animation(30, 33, 0.2),
        "sliding": Animation(19, 21, 0.2),
    }

    world = World()
    sprite_sheet_metadata = SpriteSheetMetadata(
        "resources/sprites/fred.png", 5888, 128, 46, 1
    )
    pet = Pet(sprite_sheet_metadata, animations)
    screen = pet.primaryScreen()
    update_pet_position = partial(world.update_entity_position, "pet")
    pet.on_position_updated = update_pet_position
    pet.set_animation("sliding")

    event_manager.subscribe("animation", pet.set_animation)
    event_manager.subscribe("movement", pet.set_movement)

    event_loop()
    pet.gui_loop()
    pet._image_update_timer.cancel()
    pet._image_update_timer.join()
    pet._position_update_timer.cancel()
    pet._position_update_timer.join()


if __name__ == "__main__":
    main()
