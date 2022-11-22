import math
from typing import Sequence

from .coordinate import Coordinate
from .movement import Movement


class ComposedMovement(Movement):
    def __init__(self, movements: Sequence[Movement]) -> None:
        super().__init__()
        self._movements = movements

    def _aggregate_positions(self, positions: Sequence[Coordinate]) -> Coordinate:
        n_movements = len(self._movements)
        mean_x = math.fsum((position.x for position in positions)) / n_movements
        mean_y = math.fsum((position.y for position in positions)) / n_movements
        current_position = Coordinate(mean_x, mean_y)

        return current_position

    def step(self) -> Coordinate:
        positions = tuple(movement.step() for movement in self._movements)
        current_position = self._aggregate_positions(positions)
        return current_position

    def step_reverse(self) -> Coordinate:
        positions = tuple(movement.step_reverse() for movement in self._movements)
        current_position = self._aggregate_positions(positions)
        return current_position

    def is_at_beginning(self) -> bool:
        beginnings = tuple(movement.is_at_beginning() for movement in self._movements)
        return all(beginnings)

    def is_at_endding(self) -> bool:
        enddings = tuple(movement.is_at_endding() for movement in self._movements)
        return all(enddings)
