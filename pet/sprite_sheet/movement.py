from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import NamedTuple, Sequence, Union

Numeric = Union[int, float]


class Coordinate(NamedTuple):
    x: Numeric
    y: Numeric


@dataclass
class Movement(abc.ABC):
    @abc.abstractmethod
    def step(self) -> Coordinate:
        ...

    @abc.abstractmethod
    def step_reverse(self) -> Coordinate:
        ...

    @abc.abstractmethod
    def is_at_beginning(self) -> bool:
        ...

    @abc.abstractmethod
    def is_at_endding(self) -> bool:
        ...


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


@dataclass
class LinearMovement(Movement):
    start: Coordinate
    end: Coordinate
    n_steps: int
    loop: bool = False
    loop_reverse: bool = False
    _position: Coordinate = field(default_factory=lambda: Coordinate(0, 0), init=False)
    _step_index: int = field(default=0, init=False)
    step_increment: int = field(default=1, init=False)

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
        loop: bool = False,
        loop_reverse: bool = False,
    ):
        start = Coordinate(*start)
        end = Coordinate(*end)
        return cls(start, end, n_steps, loop, loop_reverse)

    @classmethod
    def from_numeric(
        cls,
        start_x: Numeric,
        start_y: Numeric,
        end_x: Numeric,
        end_y: Numeric,
        n_steps: int,
        loop: bool = False,
        loop_reverse: bool = False,
    ):
        start = Coordinate(start_x, start_y)
        end: Coordinate = Coordinate(end_x, end_y)
        return cls(start, end, n_steps, loop, loop_reverse)

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

        is_edge_case = self._position == self.end or self._position == self.start
        if self.loop and is_edge_case:
            if self.loop_reverse:
                self.step_increment = self.step_increment * -1
                # self._step_index
            else:
                self._step_index = 0

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
