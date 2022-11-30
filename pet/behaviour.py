from dataclasses import dataclass, field

from .movement import Movement
from .sprite_sheet.animation import Animation


@dataclass
class Behaviour:
    _movement: Movement
    _animation: Animation

    def m 