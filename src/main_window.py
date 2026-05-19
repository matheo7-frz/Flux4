"""Fenetre principale de l'application avec navigation laterale et fonctions systeme."""

import threading
import webbrowser

from PySide6.QtCore import Qt, QTimer, Signal, QObject
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.config import Config
from src.core.emulator_manager import EmulatorManager
from src.core.firmware_manager import FirmwareManager
from src.core.game_library import GameLibrary
from src.core.updater import APP_VERSION, check_for_updates, UpdateInfo
from src.pages.firmware import FirmwarePage
from src.pages.home import HomePage
from src.pages.library import LibraryPage
from src.pages.settings import SettingsPage
from src.styles import COLORS, MAIN_STYLESHEET


NAV_ITEMS = [
    ("home", "Accueil"),
    ("firmware", "Firmware"),
    ("library", "Bibliothèque"),
    ("settings", "Paramètres"),
]

NAV_ICONS = {
    "home": "\u2302",
    "firmware": "\u2699",
    "library": "\u25a6",
    "settings": "\u2630",
}


class _UpdateSignal(QObject):
    """Signal pour communiquer les resultats de mise a jour depuis un thread."""

    update_checked = Signal(object)


class MainWindow(QMainWindow):
    """Fenetre principale avec barre laterale style PS4."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Flux4 - Lanceur PS4")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 780)

        self.setStyleSheet(MAIN_STYLESHEET)

        self._config = Config()
        self._firmware_mgr = FirmwareManager(self._config)
        self._emulator_mgr = EmulatorManager(self._config)
        self._game_lib = GameLibrary(self._config)

        self._nav_buttons: dict[str, QPushButton] = {}
        self._current_page = "home"
        self._update_signal = _UpdateSignal()
        self._update_signal.update_checked.connect(self._on_update_result)

        self._setup_ui()
        self._navigate_to("home")

        QTimer.singleShot(500, self._auto_scan_games)
        if self._config.check_updates:
            QTimer.singleShot(1000, self._check_for_updates)

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        logo_label = QLabel("FLUX4")
        logo_label.setObjectName("sidebar_title")
        sidebar_layout.addWidget(logo_label)

        subtitle_label = QLabel("Lanceur PS4")
        subtitle_label.setObjectName("sidebar_subtitle")
        sidebar_layout.addWidget(subtitle_label)

        for key, label in NAV_ITEMS:
            icon = NAV_ICONS.get(key, "")
            btn = QPushButton(f"  {icon}  {label}")
            btn.setObjectName("nav_button")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(44)
            btn.clicked.connect(lambda checked=False, k=key: self._navigate_to(k))
            sidebar_layout.addWidget(btn)
            self._nav_buttons[key] = btn

        sidebar_layout.addStretch()

        self._update_btn = QPushButton("  Mise à jour disponible !")
        self._update_btn.setVisible(False)
        self._update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_btn.setStyleSheet(
            f"background-color: {COLORS['success']}; color: #000; "
            f"font-weight: bold; margin: 8px; border-radius: 6px; padding: 8px;"
        )
        sidebar_layout.addWidget(self._update_btn)

        version_label = QLabel(f"  v{APP_VERSION}")
        version_label.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 10px; padding: 10px 16px;"
        )
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(sidebar)

        page_container = QFrame()
        page_container.setObjectName("page_container")
        page_layout = QVBoxLayout(page_container)
        page_layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        page_layout.addWidget(self._stack)

        self._home_page = HomePage(
            self._config, self._firmware_mgr, self._emulator_mgr, self._game_lib
        )
        self._home_page.navigate_to.connect(self._navigate_to)

        self._firmware_page = FirmwarePage(self._config, self._firmware_mgr)
        self._library_page = LibraryPage(self._config, self._game_lib, self._emulator_mgr)
        self._settings_page = SettingsPage(self._config, self._emulator_mgr)

        self._pages = {
            "home": self._home_page,
            "firmware": self._firmware_page,
            "library": self._library_page,
            "settings": self._settings_page,
        }

        for page in self._pages.values():
            self._stack.addWidget(page)

        main_layout.addWidget(page_container)

    def _navigate_to(self, page_key: str) -> None:
        """Naviguer vers une page specifique."""
        if page_key not in self._pages:
            return

        self._current_page = page_key

        for key, btn in self._nav_buttons.items():
            if key == page_key:
                btn.setObjectName("nav_button_active")
            else:
                btn.setObjectName("nav_button")
            btn.setStyleSheet("")

        page = self._pages[page_key]
        self._stack.setCurrentWidget(page)
        if hasattr(page, "refresh"):
            page.refresh()

    def _auto_scan_games(self) -> None:
        """Scanner automatiquement le dossier de jeux au demarrage."""
        scan_dir = self._config.auto_scan_directory
        if not scan_dir:
            scan_dir = self._config.games_directory
        if scan_dir:
            self._game_lib.scan_directory(scan_dir)

    def _check_for_updates(self) -> None:
        """Verifier les mises a jour en arriere-plan."""
        def _do_check() -> None:
            result = check_for_updates()
            self._update_signal.update_checked.emit(result)

        thread = threading.Thread(target=_do_check, daemon=True)
        thread.start()

    def _on_update_result(self, info: UpdateInfo) -> None:
        """Traiter le resultat de la verification de mise a jour."""
        if info.available:
            self._update_btn.setVisible(True)
            self._update_btn.setText(f"  v{info.latest_version} disponible !")
            self._update_btn.clicked.connect(
                lambda: webbrowser.open(info.release_url)
            )
            self._home_page.set_update_info(info)
