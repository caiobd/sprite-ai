from time import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from sprite_ai.event_manager import EventManager
from sprite_ai.ui.chat_window_ui import Ui_Form
from sprite_ai.ui.message_delegate import MessageDelegate

from sprite_ai.ui.message_model import MessageModel

USER_ME = 0
USER_THEM = 1

class ChatWindow(QtWidgets.QWidget):
    ai_message_recived = pyqtSignal(dict)

    def __init__(self, event_manager: EventManager):
        super().__init__()

        self.event_manager = event_manager
        self.ui = Ui_Form()
        self.model = MessageModel()

        self.ui.setupUi(self)
        self.ui.lv_chat_history.setItemDelegate(MessageDelegate())
        self.ui.lv_chat_history.setModel(self.model)
        self.ai_message_recived.connect(self.send_ai_message)
        self.ui.pb_send.clicked.connect(self.send_user_message)
        self.event_manager.subscribe('ai_message', self.ai_message_recived.emit)
    
    @pyqtSlot()
    def send_user_message(self):
        user_message = self.ui.te_chatinput.toPlainText()
        self.model.add_message(USER_ME, user_message)
        self.event_manager.publish('user_message', message={
            'timestamp': time(),
            'content': user_message,
        })
        self.ui.te_chatinput.clear()

    @pyqtSlot(dict)
    def send_ai_message(self, message: dict):
        timestamp = message['timestamp']
        content = message['content']
        self.model.add_message(USER_THEM, content)
