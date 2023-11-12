from __future__ import annotations

from dataclasses import dataclass, field

from .coordinate import Coordinate
from .movement import Movement
from .typing_utils import Numeric


@dataclass
class LinearMovement(Movement):
    start: Coordinate
    end: Coordinate
    n_steps: int
    _position: Coordinate = field(default_factory=lambda: Coordinate(0, 0), init=False)
    _step_index: int = field(default=0, init=False)
    step_increment: int = field(default=1, init=False)

    @property
    def orientation(self) -> str:
        orientation = "right"
        if self.start.x > self.end.x:
            orientation = "left"

        return orientation

    @property
    def position(self) -> Coordinate | None:
        return self._position

    @property
    def step_index(self) -> int:
        return self._step_index

    @step_index.setter
    def step_index(self, value: int):
        self._step_index = value
        self._update_position()

    def __post_init__(self):
        self._position = self.start

        if self.n_steps < 2:
            raise ValueError(
                f"value {self.n_steps} is invalid for parameter n_steps,"
                " value must be equal or greater than 2"
            )

    def __next__(self):
        yield self.step()

    @classmethod
    def from_tuple(
        cls,
        start: tuple[Numeric, Numeric],
        end: tuple[Numeric, Numeric],
        n_steps: int,
    ):
        start = Coordinate(*start)
        end = Coordinate(*end)
        return cls(start, end, n_steps)

    @classmethod
    def from_numeric(
        cls,
        start_x: Numeric,
        start_y: Numeric,
        end_x: Numeric,
        end_y: Numeric,
        n_steps: int,
    ):
        start = Coordinate(start_x, start_y)
        end: Coordinate = Coordinate(end_x, end_y)
        return cls(start, end, n_steps)

    def _update_position(self):
        if self._step_index == 0:
            # Fix float sum rounding error at start
            position = self.start
        elif self._step_index == self.n_steps - 1:
            # Fix float sum rounding error at end
            position = self.end
        else:
            # Calculate position in intermidiate steps (between start and end points)
            step_size_x = (self.end.x - self.start.x) / (self.n_steps - 1)
            step_size_y = (self.end.y - self.start.y) / (self.n_steps - 1)

            position_x = self.start.x + self._step_index * step_size_x
            position_y = self.start.y + self._step_index * step_size_y
            position = Coordinate(position_x, position_y)

        self._position = position

    def step(self) -> Coordinate:
        max_index = self.n_steps - 1
        min_index = 0

        # Makes sure _step_index respects index upper bound
        if self._step_index + self.step_increment > max_index:
            self._step_index = max_index
        # Makes sure _step_index respects index lower bound
        elif self._step_index + self.step_increment < min_index:
            self._step_index = min_index
        # Increments _step_index by step_increment amount
        else:
            self._step_index += self.step_increment

        self._update_position()

        return self._position

    def step_reverse(self) -> Coordinate:
        if self._step_index > 0:
            self._step_index -= 1
        self._update_position()

        return self._position

    def is_at_beginning(self) -> bool:
        return self._step_index == 0

    def is_at_endding(self):
        max_index = self.n_steps - 1
        return self._step_index == max_index
