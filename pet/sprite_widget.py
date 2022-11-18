from __future__ import annotations

from abc import ABC, abstractmethod

from PyQt5 import QtCore, QtWidgets


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

    def _update_image(self, evt):
        if self.image is not None:
            self._canvas.setPixmap(self.image)
            self.qwidget.update()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, xy_coordinates: tuple[int, int]):
        self._position = xy_coordinates
        if xy_coordinates is not None:
            self.qwidget.move(*xy_coordinates)

    def show(self):
        self.qwidget.show()

    def hide(self):
        self.qwidget.hide()
