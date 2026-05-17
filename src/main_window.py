"""Fenetre principale de l'application avec navigation laterale."""

from PySide6.QtCore import Qt, QSize
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
from src.pages.firmware import FirmwarePage
from src.pages.home import HomePage
from src.pages.library import LibraryPage
from src.pages.settings import SettingsPage
from src.styles import COLORS, MAIN_STYLESHEET


NAV_ITEMS = [
    ("home", "Accueil"),
    ("firmware", "Firmware"),
    ("library", "Biblioth\u00e8que"),
    ("settings", "Param\u00e8tres"),
]

NAV_ICONS = {
    "home": "\u2302",
    "firmware": "\u2699",
    "library": "\u25a6",
    "settings": "\u2630",
}


class MainWindow(QMainWindow):
    """Fenetre principale avec barre laterale style PS4."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Flux4 - Lanceur PS4")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 780)

        self.setStyleSheet(MAIN_STYLESHEET)

        # Initialize core services
        self._config = Config()
        self._firmware_mgr = FirmwareManager(self._config)
        self._emulator_mgr = EmulatorManager(self._config)
        self._game_lib = GameLibrary(self._config)

        self._nav_buttons: dict[str, QPushButton] = {}
        self._current_page = "home"

        self._setup_ui()
        self._navigate_to("home")

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Zone logo
        logo_label = QLabel("FLUX4")
        logo_label.setObjectName("sidebar_title")
        sidebar_layout.addWidget(logo_label)

        subtitle_label = QLabel("Lanceur PS4 v1.0")
        subtitle_label.setObjectName("sidebar_subtitle")
        sidebar_layout.addWidget(subtitle_label)

        # Boutons de navigation
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

        # Version en bas de la barre laterale
        version_label = QLabel("  v1.0.0")
        version_label.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 10px; padding: 10px 16px;"
        )
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(sidebar)

        # Conteneur de pages
        page_container = QFrame()
        page_container.setObjectName("page_container")
        page_layout = QVBoxLayout(page_container)
        page_layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        page_layout.addWidget(self._stack)

        # Creer les pages
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

        # Mettre a jour les styles des boutons
        for key, btn in self._nav_buttons.items():
            if key == page_key:
                btn.setObjectName("nav_button_active")
            else:
                btn.setObjectName("nav_button")
            btn.setStyleSheet("")  # force re-apply of stylesheet

        # Changer de page et rafraichir
        page = self._pages[page_key]
        self._stack.setCurrentWidget(page)
        if hasattr(page, "refresh"):
            page.refresh()
