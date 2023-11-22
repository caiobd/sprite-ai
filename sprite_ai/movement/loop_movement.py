from .coordinate import Coordinate
from .movement import Movement


class LoopMovement(Movement):
    def __init__(self, movement: Movement) -> None:
        super().__init__()
        self._movement = movement

    def step(self) -> Coordinate:
        current_position = self._movement.step()

        if self.is_at_endding():
            while not self._movement.is_at_beginning():
                current_position = self._movement.step_reverse()

        return current_position

    def step_reverse(self) -> Coordinate:
        current_position = self._movement.step_reverse()

        if self.is_at_beginning():
            while not self._movement.is_at_endding():
                current_position = self._movement.step()

        return current_position

    def is_at_beginning(self) -> bool:
        return self._movement.is_at_beginning()

    def is_at_endding(self):
        return self._movement.is_at_endding()
