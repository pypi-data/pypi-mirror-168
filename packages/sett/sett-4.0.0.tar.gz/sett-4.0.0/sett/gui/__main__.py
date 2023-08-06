#!/usr/bin/env python3
"""Secure Encryption and Transfer Tool GUI."""

import sys
import threading
import time
from typing import Any

from . import main_window
from .theme import IconRepainter, Appearance
from .pyside import QtWidgets, open_window, QtGui
from .. import APP_NAME_SHORT, __version__

# Note: rc_icon is used implicitly by PySide. It must be imported into the
# namespace, even if never used, otherwise the icons don't display in the GUI.
from .resources import rc_icons  # pylint: disable=unused-import
from ..utils.log import log_to_rotating_file


def repaint_icons(icon_repainter: IconRepainter) -> None:
    previous_appearance = Appearance.current()
    while True:
        new_appearance = Appearance.current()
        if new_appearance != previous_appearance:
            icon_repainter.repaint_icons()
            previous_appearance = new_appearance
        time.sleep(2)


def run() -> Any:
    icon_repainter = IconRepainter()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME_SHORT)
    app.setApplicationDisplayName(f"{APP_NAME_SHORT} ({__version__})")
    app.setApplicationVersion(__version__)
    app.setWindowIcon(QtGui.QIcon(":icon/sett_icon.png"))
    window = main_window.MainWindow(icon_repainter)
    log_to_rotating_file(
        log_dir=window.app_data.config.log_dir,
        file_max_number=window.app_data.config.log_max_file_number,
    )
    start_repaint_icons_thread(icon_repainter)
    window.resize(window.width() + 500, window.height())
    window.show()
    return open_window(app)


def start_repaint_icons_thread(icon_repainter: IconRepainter) -> None:
    thread = threading.Thread(target=repaint_icons, args=(icon_repainter,))
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    run()
