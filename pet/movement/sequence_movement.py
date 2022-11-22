from typing import Sequence

from .coordinate import Coordinate
from .movement import Movement


class SequenceMovement(Movement):
    def __init__(self, movements: Sequence[Movement]) -> None:
        super().__init__()
        self._movements = movements
        self._movement_index = 0

    def step(self) -> Coordinate:
        current_movement = self._movements[self._movement_index]
        current_position = current_movement.step()

        if current_movement.is_at_endding():
            self._movement_index += 1

        self._movement_index = min(self._movement_index, len(self._movements) - 1)

        return current_position

    def step_reverse(self) -> Coordinate:
        current_movement = self._movements[self._movement_index]
        current_position = current_movement.step_reverse()

        if current_movement.is_at_beginning():
            self._movement_index -= 1

        self._movement_index = max(0, self._movement_index)

        return current_position

    def is_at_beginning(self) -> bool:
        current_movement = self._movements[self._movement_index]
        is_first_index = self._movement_index == 0
        return is_first_index and current_movement.is_at_beginning()

    def is_at_endding(self) -> bool:
        current_movement = self._movements[self._movement_index]
        is_last_index = self._movement_index >= len(self._movements) - 1
        return is_last_index and current_movement.is_at_endding()
