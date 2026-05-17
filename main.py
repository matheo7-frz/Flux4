#!/usr/bin/env python3
"""PS4 Emu Launcher - A desktop frontend for shadPS4 emulator."""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("PS4 Emu Launcher")
    app.setOrganizationName("PS4EmuLauncher")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
