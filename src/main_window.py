"""Main application window with sidebar navigation."""

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
    ("home", "Home"),
    ("firmware", "Firmware"),
    ("library", "Library"),
    ("settings", "Settings"),
]

NAV_ICONS = {
    "home": "\u2302",
    "firmware": "\u2699",
    "library": "\u25a6",
    "settings": "\u2630",
}


class MainWindow(QMainWindow):
    """Main application window with PS4-styled sidebar and page stack."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PS4 Emu Launcher - shadPS4 Frontend")
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

        # Logo area
        logo_label = QLabel("PS4 Emu Launcher")
        logo_label.setObjectName("sidebar_title")
        sidebar_layout.addWidget(logo_label)

        subtitle_label = QLabel("shadPS4 Frontend v1.0")
        subtitle_label.setObjectName("sidebar_subtitle")
        sidebar_layout.addWidget(subtitle_label)

        # Navigation buttons
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

        # Version info at bottom of sidebar
        version_label = QLabel("  v1.0.0")
        version_label.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 10px; padding: 10px 16px;"
        )
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(sidebar)

        # Page container
        page_container = QFrame()
        page_container.setObjectName("page_container")
        page_layout = QVBoxLayout(page_container)
        page_layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        page_layout.addWidget(self._stack)

        # Create pages
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
        """Navigate to a specific page."""
        if page_key not in self._pages:
            return

        self._current_page = page_key

        # Update nav button styles
        for key, btn in self._nav_buttons.items():
            if key == page_key:
                btn.setObjectName("nav_button_active")
            else:
                btn.setObjectName("nav_button")
            btn.setStyleSheet("")  # force re-apply of stylesheet

        # Switch page and refresh
        page = self._pages[page_key]
        self._stack.setCurrentWidget(page)
        if hasattr(page, "refresh"):
            page.refresh()
