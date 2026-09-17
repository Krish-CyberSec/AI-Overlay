import sys

from PySide6.QtWidgets import QApplication

from app.ui.overlay import OverlayWindow
from app.windows.hotkey import GlobalHotkey


def main():
    app = QApplication(sys.argv)

    window = OverlayWindow()
    window.show()

    hotkey = GlobalHotkey(window.toggle_visibility)
    hotkey.start()

    exit_code = app.exec()

    hotkey.stop()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()