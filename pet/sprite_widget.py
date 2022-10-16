from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtCore
import sys
import logging

from pet.physics import RigidBody
from .sprite_sheet import AnimationController

# class SpriteWidget(QtWidgets.QWidget)

class AnimatedSpriteWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = None
        self.animation_controller = None
        self.frame_update_timer = None
        self.animation_duration_timer = None
        self._setup_gui()
        self._create_timers()
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

    def _create_timers(self):
        self.frame_update_timer = QTimer(self)
        self.animation_duration_timer = QTimer(self)

        self.frame_update_timer.timeout.connect(self._update_sprite)
        self.animation_duration_timer.timeout.connect(self.end_animation)

    def set_sprite_sheet(
        self,
        sprite_sheet_path: str,
        n_columns: int,
        n_rows: int,
        start_index: int = 0,
        end_index: int = None,
    ):
        sprite_sheet_image = QPixmap(sprite_sheet_path)
        self.animation_controller = AnimationController(
            sprite_sheet_image,
            n_columns,
            n_rows,
            start_index,
            end_index,
        )
        (
            _,
            _,
            frame_width,
            frame_height,
        ) = self.animation_controller.sprite_sheet_position
        self.rigid_body.width=frame_width
        self.rigid_body.height=frame_height
        

    def _update_sprite(self):
        self.animation_controller.next_frame()

    # Overrides paintEvent from QWidget
    def paintEvent(self, evt):
        self.animation_controller.draw_frame()
        frame = self.animation_controller.frame
        self.canvas.setPixmap(frame)
        self.update()

    def play(self, speed: int, duration: int = None):
        self.frame_update_timer.start(speed)
        if duration is not None:
            self.animation_duration_timer.start(duration)

    def end_animation(self):
        self.animation_duration_timer.stop()
        self.frame_update_timer.stop()
        sys.exit(0)

    def stop(self):
        self.frame_update_timer.stop()
