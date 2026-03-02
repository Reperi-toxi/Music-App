from PyQt6.QtWidgets import QListWidget, QStyledItemDelegate, QApplication
from PyQt6.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve, pyqtProperty, QPoint
from PyQt6.QtGui import QPainter, QColor, QFont, QLinearGradient, QPen, QFontMetrics

from .styles import LIST_WIDGET_STYLE

class SongItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hovered_row = -1

    def set_hovered(self, row: int):
        self._hovered_row = row

    def sizeHint(self, option, index):
        return __import__('PyQt6.QtCore', fromlist=['QSize']).QSize(0, 52)

    def paint(self, painter, option, index):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        row = index.row()
        is_selected = option.state & __import__('PyQt6.QtWidgets', fromlist=['QStyle']).QStyle.StateFlag.State_Selected
        is_hovered = row == self._hovered_row
        is_playing = index.data(Qt.ItemDataRole.UserRole + 1)  # set this flag on current song

        rect = QRectF(option.rect).adjusted(6, 4, -6, -4)

        if is_selected:
            bg = QLinearGradient(rect.left(), 0, rect.right(), 0)
            bg.setColorAt(0, QColor(120, 80, 255, 80))
            bg.setColorAt(1, QColor(80, 40, 200, 40))
            painter.setBrush(bg)
            painter.setPen(QPen(QColor(150, 110, 255, 160), 1))
        elif is_hovered:
            painter.setBrush(QColor(120, 80, 255, 30))
            painter.setPen(QPen(QColor(120, 80, 255, 60), 1))
        else:
            painter.setBrush(QColor(255, 255, 255, 5))
            painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRoundedRect(rect, 8, 8)

        if is_playing:
            bar_rect = QRectF(rect.left() + 1, rect.top() + 8, 3, rect.height() - 16)
            painter.setBrush(QColor(180, 130, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(bar_rect, 2, 2)

        num_rect = QRectF(rect.left() + 12, rect.top(), 28, rect.height())
        num_font = QFont("Consolas", 9)
        painter.setFont(num_font)
        painter.setPen(QColor(120, 100, 180, 150) if not is_selected else QColor(180, 150, 255, 200))
        painter.drawText(num_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                         f"{row + 1:02d}")

        title = index.data(Qt.ItemDataRole.DisplayRole) or ""
        title_rect = QRectF(rect.left() + 46, rect.top(), rect.width() - 80, rect.height())

        title_font = QFont("Segoe UI", 11)
        title_font.setWeight(QFont.Weight.DemiBold if is_selected else QFont.Weight.Normal)
        painter.setFont(title_font)
        painter.setPen(QColor(230, 228, 255) if is_selected else QColor(190, 185, 220))

        fm = QFontMetrics(title_font)
        elided = fm.elidedText(title, Qt.TextElideMode.ElideRight, int(title_rect.width()))
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, elided)

        # --- Music note icon on the right when playing ---
        if is_playing:
            note_font = QFont("Segoe UI", 13)
            painter.setFont(note_font)
            painter.setPen(QColor(180, 130, 255, 200))
            note_rect = QRectF(rect.right() - 30, rect.top(), 24, rect.height())
            painter.drawText(note_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, "♪")


class ListWidgetUI(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._delegate = SongItemDelegate(self)
        self.setItemDelegate(self._delegate)
        self.setMouseTracking(True)
        self.setStyleSheet(LIST_WIDGET_STYLE)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        self._delegate.set_hovered(index.row() if index.isValid() else -1)
        self.viewport().update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._delegate.set_hovered(-1)
        self.viewport().update()
        super().leaveEvent(event)

    def mark_playing(self, row: int):
        for i in range(self.count()):
            item = self.item(i)
            item.setData(Qt.ItemDataRole.UserRole + 1, i == row)
        self.viewport().update()