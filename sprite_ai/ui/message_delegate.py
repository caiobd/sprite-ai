from PyQt5.QtCore import QMargins, QPoint, Qt
from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: '#90caf9', USER_THEM: '#a5d6a7'}

BUBBLE_PADDING = QMargins(15, 5, 15, 5)
TEXT_PADDING = QMargins(25, 15, 25, 15)


class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    def paint(self, painter, option, index):
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.

        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        # draw the triangle bubble-pointer, starting from

        if user == USER_ME:
            p1 = bubblerect.topRight()
        else:
            p1 = bubblerect.topLeft()
        painter.drawPolygon(
            p1 + QPoint(-20, 0), p1 + QPoint(20, 0), p1 + QPoint(0, 20)
        )

        # draw the text
        painter.setPen(Qt.black)
        painter.drawText(textrect, Qt.TextWordWrap, text)

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        # Calculate the dimensions the text will require.
        metrics = QApplication.fontMetrics()
        rect = option.rect.marginsRemoved(TEXT_PADDING)
        rect = metrics.boundingRect(rect, Qt.TextWordWrap, text)
        rect = rect.marginsAdded(TEXT_PADDING)  # Re add padding for item size.
        return rect.size()
