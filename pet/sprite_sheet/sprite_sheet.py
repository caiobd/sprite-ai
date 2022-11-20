from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

PositionTuple = Tuple[int, int, int, int]


@dataclass
class SpriteSheetMetadata:
    path: str | Path
    width: int
    height: int
    n_columns: int
    n_rows: int

    @property
    def sprite_width(self) -> int:
        return int(self.width / self.n_columns)

    @property
    def sprite_height(self) -> int:
        return int(self.height / self.n_rows)


@dataclass
class SpriteSheetIterator:
    sprite_sheet_metadata: SpriteSheetMetadata
    start_index: int = 0
    end_index: int = None
    frame_index: int = field(init=False, default=None)

    def __post_init__(self):
        if self.end_index is None:
            self.end_index = (
                self.sprite_sheet_metadata.n_cols * self.sprite_sheet_metadata.n_rows
            )
        self.frame_index = self.start_index

        assert self.start_index <= self.end_index, "Invalid start index"
        assert (
            self.end_index
            <= self.sprite_sheet_metadata.n_columns * self.sprite_sheet_metadata.n_rows
        ), "Invalid end index"

    def _update_frame_index(self):
        if self.frame_index >= self.end_index - 1:
            self.frame_index = self.start_index
        else:
            self.frame_index += 1

    def __iter__(self):
        return self

    def __next__(self) -> PositionTuple:
        self._update_frame_index()
        return self.position

    def reset(self):
        self.frame_index = self.start_index

    def increment(self):
        return next(self)

    @property
    def position(self) -> PositionTuple:
        return (
            self.offset_x,
            self.offset_y,
            self.sprite_sheet_metadata.sprite_width,
            self.sprite_sheet_metadata.sprite_height,
        )

    @property
    def offset_x(self) -> int:
        try:
            _offset_x = (
                self.sprite_sheet_metadata.sprite_width
                * self.frame_index
                % self.sprite_sheet_metadata.width
            )
        except:
            _offset_x = 0
        return _offset_x

    @property
    def offset_y(self) -> int:
        try:
            _offset_y = (
                self.sprite_sheet_metadata.sprite_height
                * self.frame_index
                % self.sprite_sheet_metadata.sprite_width
            )
        except:
            _offset_y = 0

        return _offset_y
