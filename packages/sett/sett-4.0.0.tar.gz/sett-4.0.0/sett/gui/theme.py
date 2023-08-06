from enum import Enum
from typing import Callable, cast

import darkdetect

from .pyside import QtGui, get_application_global_instance, QtCore, QtWidgets, QAction


class Appearance(Enum):
    LIGHT = 1
    DARK = 2

    @classmethod
    def current(cls) -> "Appearance":
        return cls.DARK if darkdetect.isDark() else cls.LIGHT


class Icon(QtGui.QIcon):
    def __init__(self, filename: str):
        super().__init__(self.to_pixmap(filename))

    @staticmethod
    def to_pixmap(filename: str) -> QtGui.QPixmap:
        palette = get_application_global_instance().palette()  # type: ignore
        pixmap = QtGui.QPixmap(filename)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), palette.color(palette.ColorRole.Text))
        painter.end()
        return pixmap


class IconRepainter(QtCore.QObject):
    signal = QtCore.Signal()

    def repaint_icons(self) -> None:
        self.signal.emit()

    def register(self, slot: Callable[..., None]) -> None:
        self.signal.connect(slot)


class IconRepainterWidget(QtWidgets.QWidget):
    def icon_repainter(self) -> IconRepainter:
        if hasattr(self, "_icon_repainter"):
            return cast(IconRepainter, self._icon_repainter)  # type: ignore
        parent_widget = self.parentWidget()
        if parent_widget and isinstance(self, IconRepainterWidget):
            return cast(IconRepainterWidget, parent_widget).icon_repainter()
        raise NotImplementedError(f"'_icon_repainter' NOT found in '{type(self)}'")


class Action(QAction):
    def __init__(
        self, icon_file_name: str, text: str, parent: IconRepainterWidget
    ) -> None:
        self._icon_file_name = icon_file_name
        super().__init__(Icon(icon_file_name), text, parent)
        parent.icon_repainter().register(self.refresh_icon)

    def refresh_icon(
        self,
    ) -> None:
        self.setIcon(Icon(self._icon_file_name))


class PushButton(QtWidgets.QPushButton):
    def __init__(
        self, icon_file_name: str, text: str, parent: IconRepainterWidget
    ) -> None:
        self._icon_file_name = icon_file_name
        super().__init__(Icon(icon_file_name), text, parent)
        parent.icon_repainter().register(self.refresh_icon)

    def refresh_icon(self) -> None:
        self.setIcon(Icon(self._icon_file_name))
