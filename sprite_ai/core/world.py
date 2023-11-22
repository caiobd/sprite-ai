from __future__ import annotations

import threading
from time import time
from typing import Any

from loguru import logger

from sprite_ai.event_manager import EventManager

# from pet.core.pet import Pet


class World:
    def __init__(self, world_size) -> None:
        self.world_size = world_size
        self.entities: dict[str, Any] = {}
        self.event_manager = EventManager()
        self.world_clock_timer = None
        self.last_target = None
        self.world_clock_loop()

    def update_entity_position(self, entity_name, position_update_message):
        new_position = position_update_message["new_position"]
        old_position = position_update_message["old_position"]

        self.entities[entity_name] = position_update_message["new_position"]

    def world_clock_loop(self):
        self.world_clock_timer = threading.Timer(1, self.world_clock_loop)
        self.world_clock_timer.start()

        current_time = round(time())
        self.event_manager.publish("world_clock", current_time)

    def update_state_event(self, clock_time: int, pet: Pet):
        if clock_time % 5 == 0:
            pet.next_state()
            logger.debug(f"<new state> {pet.get_state()}")
