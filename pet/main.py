from __future__ import annotations

from pet.sprite_sheet.animation import Animation
from pet.sprite_sheet.movement import LinearMovement
from pet.sprite_sheet.sprite_sheet import SpriteSheetMetadata
from pet.sprite_widget import AnimatedSpriteWidget
from PyQt5 import QtWidgets
import sys


class Pet:
    def __init__(self, sprite_sheet_metadata: SpriteSheetMetadata, animations: dict) -> None:
        self._app = QtWidgets.QApplication(sys.argv)
        self.sprite_widget = AnimatedSpriteWidget()
        self.sprite_widget.set_sprite_sheet(sprite_sheet_metadata, animations)
    
    def event_loop(self):
        self.sprite_widget.show()
        self.sprite_widget.set_animation('jumping')
        self.sprite_widget.play_animation()
        self.sprite_widget.set_postion(500,500)
        self._app.exec()



def main():
    animations = {
        'idle': Animation(0, 0, 0.2),
        'walking': Animation(0, 3, 0.2),
        'jumping': Animation(2, 4, 0.2),
    }
    movements = {
        'idle': [],
        'walking': [LinearMovement.from_tuple((0, 0), (1, 0), 500, loop=True)],
        'jumping': [LinearMovement.from_tuple((0, 0), (0, 0.2), 500, loop=True)],
    }

    sprite_sheet_metadata = SpriteSheetMetadata(
        "resources/sprites/fred.png", 5888, 128, 46, 1
    )
    pet = Pet(sprite_sheet_metadata, animations)
    pet.event_loop()


if __name__ == "__main__":
    main()
