from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional

from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class EventDispatcher:
    """Install a native event filter to receive events from the OS"""

    def __init__(self, keybinder) -> None:
        self.win_event_filter = WinEventFilter(keybinder)
        self.event_dispatcher = QAbstractEventDispatcher.instance()
        self.event_dispatcher.installNativeEventFilter(self.win_event_filter)


class QtKeyBinder:
    def __init__(self, win_id: Optional[int]) -> None:
        keybinder.init()
        self.win_id = win_id

        self.event_dispatcher = EventDispatcher(keybinder=keybinder)

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        keybinder.register_hotkey(self.win_id, hotkey, callback)

    def unregister_hotkey(self, hotkey: str) -> None:
        keybinder.unregister_hotkey(self.win_id, hotkey)


class ShortcutManager:
    def __init__(self) -> None:
        self.thread_pool = ThreadPoolExecutor(max_workers=1)
        self.key_binder = QtKeyBinder(win_id=None)

    def register_shortcut(self, hotkey: str, callback: Callable):
        self.key_binder.register_hotkey(
            hotkey, lambda: self.thread_pool.submit(callback)
        )
