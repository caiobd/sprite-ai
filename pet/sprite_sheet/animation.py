from dataclasses import dataclass, field
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from pet import sprite_sheet
from .sprite_sheet import SpriteSheetInfo, SpriteSheetIterator
import logging

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
    speed: int
    duration: int
    sprite_sheet_info: SpriteSheetInfo
    iterator: SpriteSheetIterator = field(init=False)

    def __post_init__(self):
        self.iterator = SpriteSheetIterator(
            self.sprite_sheet_info, 
            self.start_index,
            self.end_index,
        )

# sprite renderer
class AnimationController:
    def __init__(
        self,
        sprite_sheet_image: QPixmap,
        sprite_sheet_n_columns: int,
        sprite_sheet_n_rows: int,
        start_index: int = 0,
        end_index: int = None,
    ):
        self.sprite_sheet_image = sprite_sheet_image
        self.sprite_sheet_info = SpriteSheetInfo.from_qpixmap(
            sprite_sheet_image, sprite_sheet_n_columns, sprite_sheet_n_rows
        )
        self.canvas_image = QPixmap(
            self.sprite_sheet_info.sprite_width, self.sprite_sheet_info.sprite_height
        )
        self.sprite_sheet_iterator = SpriteSheetIterator(
            self.sprite_sheet_info,
            start_index,
            end_index,
        )
        self.sprite_sheet_position = next(self.sprite_sheet_iterator)
    
    def set_animation(name: str):
        try:
            self._animation = self._animations[name]
        except KeyError as ke:
            logging.error(ke)


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
        self.canvas_image.fill(Qt.transparent)
        (
            spritesheet_x_offset,
            spritesheet_y_offset,
            frame_width,
            frame_height,
        ) = self.sprite_sheet_position
        painter = QPainter(self.canvas_image)
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
