from pathlib import Path
from time import time
from typing import Callable

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, Qt, pyqtSignal, pyqtSlot
from sprite_ai.language.chat_message import ChatMessage

from sprite_ai.ui.chat_window_ui import Ui_MainWindow
from sprite_ai.ui.message_delegate import MessageDelegate
from sprite_ai.ui.message_model import MessageModel

USER_ME = 0
USER_THEM = 1


class ChatWindow(QtWidgets.QMainWindow):
    message_recived = pyqtSignal(dict)

    def __init__(
        self,
        on_clear_chat: Callable,
        on_user_message: Callable,
        on_open_settings: Callable,
        on_exit: Callable,
    ):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.model = MessageModel()

        self.ui.setupUi(self)
        self.ui.lv_chat_history.setItemDelegate(MessageDelegate())
        self.ui.lv_chat_history.setModel(self.model)

        # This allow overriding the event filter
        self.ui.te_chatinput.installEventFilter(self)

        self.ui.a_settings.triggered.connect(self.open_settings)
        self.ui.a_clear_chat.triggered.connect(self.clear_messages)
        self.ui.a_exit.triggered.connect(self._exit_pressed)
        self.ui.pb_send.clicked.connect(self.send_user_message)
        self.message_recived.connect(self.add_message)

        self.on_clear_chat = on_clear_chat
        self.on_user_message = on_user_message
        self.on_open_settings = on_open_settings
        self.on_exit = on_exit

        self.show()
        self.hide()

    @pyqtSlot()
    def _exit_pressed(self):
        self.on_exit()

    def eventFilter(self, obj, event: QEvent):
        # Send message if enter is pressed without holding shift
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if event.type() == QEvent.KeyPress and obj is self.ui.te_chatinput:
            if (
                event.key() == Qt.Key_Return
                and self.ui.te_chatinput.hasFocus()
                and not modifiers == Qt.ShiftModifier
            ):
                self.send_user_message()

                # ignore keypress event
                return True

        return super().eventFilter(obj, event)

    @pyqtSlot()
    def send_user_message(self):
        user_message = self.ui.te_chatinput.toPlainText()
        message = ChatMessage(
            sender='user',
            timestamp=time(),
            content=user_message,
        )
        self.on_user_message(message)
        self.ui.te_chatinput.clear()

    @pyqtSlot(dict)
    def add_message(self, message: dict):
        sender = message.get('sender', '')
        if sender == 'ai':
            sender_id = USER_THEM
        elif sender == 'user':
            sender_id = USER_ME
        else:
            raise ValueError(
                f'Invalid sender "{sender}", must be "ai" or "user"'
            )

        timestamp = message['timestamp']
        content = message['content']
        self.model.add_message(sender_id, content)
        self.ui.lv_chat_history.scrollToBottom()
        self.model.layoutChanged.emit()

    @pyqtSlot()
    def clear_messages(self):
        self.on_clear_chat()
        self.model.clear_messages()

    @pyqtSlot()
    def open_settings(self):
        self.on_open_settings()
