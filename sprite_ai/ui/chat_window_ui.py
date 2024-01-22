# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/chat_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(780, 452)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lv_chat_history = QtWidgets.QListView(Form)
        self.lv_chat_history.setMinimumSize(QtCore.QSize(0, 10))
        self.lv_chat_history.setObjectName("lv_chat_history")
        self.verticalLayout_2.addWidget(self.lv_chat_history)
        self.hl_user_interface = QtWidgets.QHBoxLayout()
        self.hl_user_interface.setContentsMargins(-1, 0, -1, -1)
        self.hl_user_interface.setObjectName("hl_user_interface")
        self.te_chatinput = QtWidgets.QTextEdit(Form)
        self.te_chatinput.setMaximumSize(QtCore.QSize(16777215, 80))
        self.te_chatinput.setObjectName("te_chatinput")
        self.hl_user_interface.addWidget(self.te_chatinput)
        self.pb_send = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_send.sizePolicy().hasHeightForWidth())
        self.pb_send.setSizePolicy(sizePolicy)
        self.pb_send.setObjectName("pb_send")
        self.hl_user_interface.addWidget(self.pb_send)
        self.verticalLayout_2.addLayout(self.hl_user_interface)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sprite AI"))
        self.pb_send.setText(_translate("Form", "Send"))
