from __future__ import annotations

from time import time
from typing import Any

from loguru import logger

from sprite_ai.event_manager import EventManager


class World:
    def __init__(self, world_size: tuple[int, int]) -> None:
        self.world_size = world_size
        self.event_manager = EventManager()
