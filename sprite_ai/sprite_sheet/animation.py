from __future__ import annotations

import copy
import threading as th
from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QTransform

from .sprite_sheet import SpriteSheetIterator, SpriteSheetMetadata

# from itertools import loop
# class FrameSequence:
#     def __init__(self, frame_index_sequence:tuple[int], total_frames:int):
#         self.index_sequence = frame_index_sequence
#         self.total_frames = total_frames

#     @classmethod
#     def from_range(start_index, end_index):
#         pass

#     def next(self):
#         for frame_sequence in

# class AbstractAnimation:
#     sprite_sheet: AbstractSpriteSheet
#     renderer: AbstractRenderer
#     frame_sequence: FrameSequence


# class SpriteRenderer:
#     def __init__(
#         self,
#         sprite_sheet: object,
#         sprite_sheet_iterator: SpriteSheetIterator,
#         sprite_sheet_n_rows: int,
#         start_index: int = 0,
#         end_index: int = None,
#     ):
#         self.sprite_sheet = sprite_sheet
#         self.sprite_sheet_info = SpriteSheetInfo.from_qpixmap(
#             sprite_sheet, sprite_sheet_n_columns, sprite_sheet_n_rows
#         )
#         self.sprite_sheet_iterator = SpriteSheetIterator(
#             self.sprite_sheet_info,
#             start_index,
#             end_index,
#         )
#         self.sprite_sheet_position = None  # next(self.sprite_sheet_iterator)

#     def next(self):
#         pass

#     def render(self, canvas: object):
#         pass


@dataclass
class Animation:
    start_index: int
    end_index: int
    speed: int | float
    duration: int | float | None = None
    flip_x: bool = False
    flip_y: bool = False


# sprite renderer
class AnimationController:
    def __init__(
        self,
        sprite_sheet_image: QPixmap,
        sprite_sheet_metadata: SpriteSheetMetadata,
        animations: dict[str, Animation] | None = None,
    ):
        self.sprite_sheet_image = sprite_sheet_image
        self.sprite_sheet_metadata = sprite_sheet_metadata
        self.canvas_image = QPixmap(
            self.sprite_sheet_metadata.sprite_width,
            self.sprite_sheet_metadata.sprite_height,
        )
        self._animations = animations
        self._animation: Animation | None = None
        self.sprite_sheet_iterator = SpriteSheetIterator(
            self.sprite_sheet_metadata,
            0,
            0,
        )
        self.sprite_sheet_position = next(self.sprite_sheet_iterator)
        self._animation_loop_timer: th.Timer | None = None
        self._stop_animation_timer: th.Timer | None = None
        self.is_running = False

        self._x_flipped = False
        self._y_flipped = False
        self._orientation = "right"

    def set_animation(self, name: str, flip_x: bool = False, flip_y: bool = False):
        if self._animations == None:
            raise TypeError("Animations must be set and not None")
        try:
            animation: Animation = self._animations[name]

            animation.flip_x = flip_x
            animation.flip_y = flip_y
            self._animation = animation
            self.sprite_sheet_iterator.start_index = animation.start_index
            self.sprite_sheet_iterator.end_index = animation.end_index
            self.sprite_sheet_iterator.reset()
        except KeyError as ke:
            animation_names: list[str] = []
            animation_names = self._animations.keys()
            raise ValueError(
                f'Invalid animations name: "{name}", please use one of {animation_names}'
            )

    def _update_orientation(self):
        flip_x = self._orientation == "right"
        self._animation.flip_x = flip_x

    def set_orientation(self, orientation: str):
        self._orientation = orientation
        self._update_orientation()

    def get_orientation(self):
        return self._orientation

    def reset(self):
        self.sprite_sheet_iterator.reset()

    @property
    def animation(self) -> Animation | None:
        return self._animation

    def next_frame(self):
        self.sprite_sheet_position = next(self.sprite_sheet_iterator)

    @property
    def frame(self):
        return self.canvas_image

    def draw_frame(self):
        if not all(
            (self.canvas_image, self.sprite_sheet_image, self.sprite_sheet_position)
        ):
            return

        (
            spritesheet_x_offset,
            spritesheet_y_offset,
            frame_width,
            frame_height,
        ) = self.sprite_sheet_position
        self.canvas_image.fill(Qt.transparent)

        painter: QPainter = QPainter(self.canvas_image)
        painter.drawPixmap(
            0,
            0,
            frame_height,
            frame_height,
            self.sprite_sheet_image,
            spritesheet_x_offset,
            spritesheet_y_offset,
            frame_width,
            frame_height,
        )
        self._update_flip_state(painter)

    def _update_flip_state(self, painter):
        x_transform = 1
        y_transform = 1

        if self._animation.flip_x:
            x_transform = -1
        if self._animation.flip_y:
            y_transform = -1

        image_transform = QTransform.fromScale(x_transform, y_transform)

        transformed_canvas_image = self.canvas_image.transformed(image_transform)
        self.canvas_image.fill(Qt.transparent)
        painter.drawPixmap(0, 0, transformed_canvas_image)

    def _start_animation_loop(self):
        self._animation_loop_timer = th.Timer(
            self.animation.speed, self._start_animation_loop
        )
        self._animation_loop_timer.start()
        self.next_frame()
        self.draw_frame()

    def _stop_animation_loop(self):
        self._animation_loop_timer.cancel()

    def play(self):
        if self._animation == None:
            raise ValueError("animation must be set before play is called")
        self.is_animation_running = True
        self._start_animation_loop()
        self._stop_animation_timer = th.Timer(
            self._animation.duration, self._stop_animation_loop
        )
        self._stop_animation_timer.start()

    def stop(self):
        self._stop_animation_timer.cancel()
        self._stop_animation_loop()
        self.is_animation_running = False


# class Renderer:
#     def render(self, canvas_x, canvas_y, image: Image, frame_x: int, frame_y: int, frame_width: int, frame_height: int):
#         pass

# class Canvas:
#     pass

# class Image:
#     pass


# class QPainterRendererAdapter(Renderer):
#     def __init__(self, canvas: QPixmap):
#         self.qpainter = QPainter(canvas)
#         self.canvas = canvas

#     def render(self, canvas_x, canvas_y, image: Image, image_x_offset: int, image_y_offset: int, image_width: int, image_height: int):

#         if not image.isinstance(QPixmap):
#             raise TypeError("Unsuported image type, try using QPixmap")

#         self.qpainter.drawPixmap(
#             canvas_x,
#             canvas_y,
#             image_width,
#             image_height,
#             image,
#             image_x_offset,
#             image_y_offset,
#             image_width,
#             image_height,
#         )
