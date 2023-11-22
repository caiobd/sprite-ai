from __future__ import annotations

import abc
from dataclasses import dataclass

from .coordinate import Coordinate


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
