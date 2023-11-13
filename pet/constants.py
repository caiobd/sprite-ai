from __future__ import annotations
from plyer.utils import platform
from importlib import resources


APP_NAME = "Pet"
ICON_EXTENTION = icon_extension = "ico" if platform == "win" else "png"
ICON_FILE = str(resources.path("pet.resources.icons", f"icon.{ICON_EXTENTION}"))
