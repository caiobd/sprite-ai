from typing import NamedTuple

from .typing_utils import Numeric


class Coordinate(NamedTuple):
    x: Numeric
    y: Numeric
