from __future__ import annotations

from abc import ABC, abstractmethod

from PyQt5 import QtCore, QtWidgets

from sprite_ai.movement.coordinate import Coordinate
from sprite_ai.movement.typing_utils import Numeric


class SpriteWidget(ABC):
    @property
    @abstractmethod
    def image(self):
        ...

    @image.setter
    @abstractmethod
    def image(self, value):
        ...

    @property
    @abstractmethod
    def position(self):
        ...

    @position.setter
    @abstractmethod
    def position(self, value):
        ...

    @abstractmethod
    def show(self):
        ...

    @abstractmethod
    def hide(self):
        ...


class SpriteWidgetQt(SpriteWidget):
    def __init__(self):
        self.qwidget = QtWidgets.QWidget()
        self._canvas = None
        self.image = None
        self._setup_gui()

    def _setup_gui(self):
        self._canvas = QtWidgets.QLabel()
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self._canvas)
        self.qwidget.setLayout(layout)
        self.qwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.qwidget.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        # Overrides paintEvent from QWidget
        self.qwidget.paintEvent = self._update_image
        self.position = (0, 0)

    def _update_image(self, evt):
        if self._canvas is not None and self.image is not None:
            self._canvas.setPixmap(self.image)
            self.qwidget.update()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def position(self) -> Coordinate:
        return self._position

    @position.setter
    def position(self, xy_coordinates: tuple[Numeric, Numeric] | Coordinate):
        x, y = xy_coordinates
        x = int(x)
        y = int(y)
        self._position = Coordinate(x, y)
        self.qwidget.move(x, y)

    def show(self):
        self.qwidget.show()

    def hide(self):
        self.qwidget.hide()
