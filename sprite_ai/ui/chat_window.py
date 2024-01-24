from time import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, Qt, pyqtSignal, pyqtSlot

from sprite_ai.event_manager import EventManager
from sprite_ai.ui.chat_window_ui import Ui_MainWindow
from sprite_ai.ui.message_delegate import MessageDelegate
from sprite_ai.ui.message_model import MessageModel

USER_ME = 0
USER_THEM = 1


class ChatWindow(QtWidgets.QMainWindow):
    message_recived = pyqtSignal(dict)

    def __init__(self, event_manager: EventManager):
        super().__init__()

        self.event_manager = event_manager
        self.ui = Ui_MainWindow()
        self.model = MessageModel()

        self.ui.setupUi(self)
        self.ui.lv_chat_history.setItemDelegate(MessageDelegate())
        self.ui.lv_chat_history.setModel(self.model)

        # This allow overriding the event filter
        self.ui.te_chatinput.installEventFilter(self)

        self.ui.a_clear_chat.triggered.connect(self.clear_messages)
        self.ui.a_exit.triggered.connect(self._exit_pressed)
        self.ui.pb_send.clicked.connect(self.send_user_message)

        self.message_recived.connect(self.add_message)
        self.event_manager.subscribe(
            'ui.chat_window.add_message', self.message_recived.emit
        )
        self.show()
        self.hide()

    @pyqtSlot()
    def _exit_pressed(self):
        self.event_manager.publish('exit')

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
        message = {
            'sender': 'user',
            'timestamp': time(),
            'content': user_message,
        }
        self.add_message(message)
        self.event_manager.publish(
            'ui.chat_window.process_user_message', message
        )
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
        self.event_manager.publish('ui.chat_window.clear')
        self.model.clear_messages()
