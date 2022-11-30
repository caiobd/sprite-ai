from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence, Tuple

from pet.sprite_sheet.animation import Animation

PositionTuple = Tuple[int, int, int, int]


class Sprite:
    def __init__(
        self,
        sprite_sheet_location: str | Path,
        width: int,
        height: int,
        n_columns: int,
        n_rows: int,
        animations: dict[str, Animation] | None = None,
        start_animation_name: str | None = None,
    ) -> None:
        self.metadata = SpriteSheetMetadata(
            sprite_sheet_location, width, height, n_columns, n_rows
        )
        if animations == None:
            animations = {}
        self._animations = animations

        self.current_animation = start_animation_name

        if self.current_animation is not None:
            self.set_animation(self.current_animation)
        else:
            self._animation: Animation | None = None

    def get_animation_names(self) -> Tuple[str, ...]:
        if self._animations == None:
            return tuple()
        return tuple(self._animations.keys())

    def set_animations(self, animations: dict[str, Animation]):
        self._animations = animations

    def get_animations(self) -> dict[str, Animation]:
        return self._animations

    def get_animation(self) -> Animation | None:
        return self._animation

    def set_animation(self, animation_name: str):
        if animation_name == None:
            raise TypeError('The value of "animation_name" cant be None')
        if self._animations == None:
            raise ValueError(f"This sprite has no animations")
        try:
            self._animation = self._animations[animation_name]
        except KeyError as ke:
            raise ValueError(f'No matching animations with name "{animation_name}"')


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
    end_index: int = -1
    frame_index: int = field(init=False, default=0)

    def __post_init__(self):
        if self.end_index == -1:
            self.end_index = (
                self.sprite_sheet_metadata.n_columns * self.sprite_sheet_metadata.n_rows
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
