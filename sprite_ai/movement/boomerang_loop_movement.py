from .coordinate import Coordinate
from .movement import Movement


class BoomerangLoopMovement(Movement):
    def __init__(self, movement: Movement) -> None:
        super().__init__()
        self._movement = movement
        self._is_reversed = False

    def _update_reversed_status(self):
        if self._movement.is_at_endding():
            self._is_reversed = True
        if self._movement.is_at_beginning():
            self._is_reversed = False

    def step(self) -> Coordinate:
        self._update_reversed_status()

        if self._is_reversed:
            current_position = self._movement.step_reverse()
        else:
            current_position = self._movement.step()

        return current_position

    def step_reverse(self) -> Coordinate:
        self._update_reversed_status()

        if self._is_reversed:
            current_position = self._movement.step()
        else:
            current_position = self._movement.step_reverse()

        return current_position

    def is_at_beginning(self) -> bool:
        return self._movement.is_at_beginning()

    def is_at_endding(self):
        return self._movement.is_at_endding()
