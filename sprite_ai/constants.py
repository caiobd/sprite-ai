from __future__ import annotations

from importlib import resources

from plyer.utils import platform

APP_NAME = "sprite-ai"
ICON_EXTENTION = icon_extension = "ico" if platform == "win" else "png"
ICON_FILE = str(resources.path("sprite_ai.resources.icons", f"icon.{ICON_EXTENTION}"))
