"""Fenetre principale avec navigation horizontale style PS4 XMB."""

import threading
import webbrowser
from datetime import datetime

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
from src.pages.home import HomePage
from src.pages.library import LibraryPage
from src.pages.settings import SettingsPage
from src.styles import COLORS, MAIN_STYLESHEET


NAV_ITEMS = [
    ("home", "Accueil", "\u25b6"),
    ("library", "Biblioth\u00e8que", "\u25a6"),
    ("settings", "Param\u00e8tres", "\u2699"),
]


class _UpdateSignal(QObject):
    """Signal pour communiquer les resultats de mise a jour depuis un thread."""

    update_checked = Signal(object)


class MainWindow(QMainWindow):
    """Fenetre principale avec menu horizontal style PS4."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("FLUX4 - Lanceur PS4")
        self.setMinimumSize(1000, 650)
        self.resize(1100, 720)

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

        self._clock_timer = QTimer()
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(30000)

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === BARRE SUPERIEURE ===
        top_bar = QFrame()
        top_bar.setObjectName("top_bar")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_layout.setSpacing(0)

        title_label = QLabel("FLUX4")
        title_label.setObjectName("top_bar_title")
        top_bar_layout.addWidget(title_label)

        top_bar_layout.addStretch()

        self._update_top_label = QLabel("")
        self._update_top_label.setVisible(False)
        self._update_top_label.setStyleSheet(
            f"color: {COLORS['success']}; font-size: 11px; "
            f"font-weight: bold; padding-right: 12px;"
        )
        self._update_top_label.setCursor(Qt.CursorShape.PointingHandCursor)
        top_bar_layout.addWidget(self._update_top_label)

        self._clock_label = QLabel(datetime.now().strftime("%H:%M"))
        self._clock_label.setObjectName("top_bar_info")
        top_bar_layout.addWidget(self._clock_label)

        main_layout.addWidget(top_bar)

        # === ZONE DE NAVIGATION HORIZONTALE ===
        nav_area = QFrame()
        nav_area.setObjectName("nav_strip")
        nav_area_layout = QVBoxLayout(nav_area)
        nav_area_layout.setContentsMargins(30, 10, 30, 0)
        nav_area_layout.setSpacing(6)

        icons_row = QHBoxLayout()
        icons_row.setSpacing(14)
        icons_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for key, label, icon in NAV_ITEMS:
            btn = QPushButton(f"{icon}\n{label}")
            btn.setObjectName("nav_icon_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(82, 82)
            btn.clicked.connect(
                lambda checked=False, k=key: self._navigate_to(k)
            )
            icons_row.addWidget(btn)
            self._nav_buttons[key] = btn

        nav_area_layout.addLayout(icons_row)

        self._selected_label = QLabel("Accueil")
        self._selected_label.setObjectName("nav_selected_label")
        self._selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_area_layout.addWidget(self._selected_label)

        main_layout.addWidget(nav_area)

        # === ZONE DE CONTENU ===
        content_area = QFrame()
        content_area.setObjectName("content_area")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        content_layout.addWidget(self._stack)

        self._home_page = HomePage(
            self._config, self._firmware_mgr, self._emulator_mgr, self._game_lib
        )
        self._home_page.navigate_to.connect(self._navigate_to)

        self._library_page = LibraryPage(
            self._config, self._game_lib, self._emulator_mgr
        )
        self._settings_page = SettingsPage(
            self._config, self._emulator_mgr, self._firmware_mgr
        )

        self._pages = {
            "home": self._home_page,
            "library": self._library_page,
            "settings": self._settings_page,
        }

        for page in self._pages.values():
            self._stack.addWidget(page)

        main_layout.addWidget(content_area, 1)

        # === BARRE INFERIEURE ===
        bottom_bar = QFrame()
        bottom_bar.setObjectName("bottom_bar")
        bottom_bar_layout = QHBoxLayout(bottom_bar)
        bottom_bar_layout.setContentsMargins(0, 0, 0, 0)
        bottom_bar_layout.setSpacing(0)

        self._fw_status_label = QLabel("")
        self._fw_status_label.setObjectName("bottom_bar_status")
        bottom_bar_layout.addWidget(self._fw_status_label)

        bottom_bar_layout.addStretch()

        version_label = QLabel(f"FLUX4 v{APP_VERSION}")
        version_label.setObjectName("bottom_bar_text")
        bottom_bar_layout.addWidget(version_label)

        main_layout.addWidget(bottom_bar)

    def _navigate_to(self, page_key: str) -> None:
        """Naviguer vers une page specifique."""
        if page_key not in self._pages:
            return

        self._current_page = page_key

        for key, btn in self._nav_buttons.items():
            if key == page_key:
                btn.setObjectName("nav_icon_btn_active")
            else:
                btn.setObjectName("nav_icon_btn")
            btn.setStyleSheet("")

        label_map = {item[0]: item[1] for item in NAV_ITEMS}
        self._selected_label.setText(label_map.get(page_key, ""))

        page = self._pages[page_key]
        self._stack.setCurrentWidget(page)
        if hasattr(page, "refresh"):
            page.refresh()

        self._update_firmware_status()

    def _update_firmware_status(self) -> None:
        """Mettre a jour le statut du firmware dans la barre inferieure."""
        fw_info = self._firmware_mgr.get_installed_firmware()
        if fw_info and fw_info.is_valid:
            version = fw_info.version or "?"
            self._fw_status_label.setText(f"Firmware : v{version}")
            self._fw_status_label.setStyleSheet(
                f"color: {COLORS['success']}; font-size: 11px; "
                f"padding: 0px 20px; font-weight: bold;"
            )
        else:
            self._fw_status_label.setText("Firmware : Non install\u00e9")
            self._fw_status_label.setStyleSheet(
                f"color: {COLORS['danger']}; font-size: 11px; "
                f"padding: 0px 20px;"
            )

    def _update_clock(self) -> None:
        self._clock_label.setText(datetime.now().strftime("%H:%M"))

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
            self._update_top_label.setVisible(True)
            self._update_top_label.setText(
                f"\u2b06 v{info.latest_version} disponible"
            )
            self._update_top_label.mousePressEvent = (
                lambda _: webbrowser.open(info.release_url)
            )
            self._home_page.set_update_info(info)
