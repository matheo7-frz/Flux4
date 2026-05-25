#!/usr/bin/env python3
"""Flux4 - Lanceur desktop pour l'emulateur PS4 shadPS4."""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Flux4")
    app.setOrganizationName("PS4EmuLauncher")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
