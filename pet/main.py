from pet.sprite_widget import AnimatedSpriteWidget
from PyQt5 import QtWidgets
import sys


def main():
    app = QtWidgets.QApplication(sys.argv)

    sprite_widget = AnimatedSpriteWidget()
    sprite_widget.set_sprite_sheet("resources/sprites/fred.png", 46, 1, 0, 3)

    sprite_widget.play(200, 50000)
    sprite_widget.show()

    app.exec()


if __name__ == "__main__":
    main()
