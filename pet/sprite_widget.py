from __future__ import annotations

from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtCore

from pet.physics import RigidBody
from pet.sprite_sheet.animation import Animation
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from .sprite_sheet import AnimationController

# class SpriteWidget(QtWidgets.QWidget)

class AnimatedSpriteWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = None
        self.animation_controller = None
        self._setup_gui()
        self.rigid_body = RigidBody(
            x=0,
            y=0,
            height=0,
            width=0,
        )

    def _setup_gui(self):
        self.canvas = QtWidgets.QLabel()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )

    def set_sprite_sheet(
        self,
        sprite_sheet_metadata: SpriteSheetMetadata,
        animations:dict[str,Animation]=None
    ):
        sprite_sheet_image = QPixmap(sprite_sheet_metadata.path)
        self.animation_controller = AnimationController(
            sprite_sheet_image,
            sprite_sheet_metadata,
            animations
        )
        (
            _,
            _,
            frame_width,
            frame_height,
        ) = self.animation_controller.sprite_sheet_position
        self.rigid_body.width=frame_width
        self.rigid_body.height=frame_height

    # Overrides paintEvent from QWidget
    def paintEvent(self, evt):
        self.update_frame()
    
    def update_frame(self):
        self.animation_controller.draw_frame()
        frame = self.animation_controller.frame
        self.canvas.setPixmap(frame)
        self.update()
    
    def set_animation(self, name:str):
        self.animation_controller.set_animation(name)
    
    def play_animation(self):
        self.animation_controller.play()
    
    def stop_animation(self):
        self.animation_controller.stop()
    
    def set_postion(self, x, y):
        self.move(x, y)
    

        