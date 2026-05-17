"""Home/Dashboard page showing system status and quick actions."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.config import Config
from src.core.emulator_manager import EmulatorManager
from src.core.firmware_manager import FirmwareManager
from src.core.game_library import GameLibrary


class StatusCard(QFrame):
    """A dashboard status card widget."""

    def __init__(self, title: str, value: str, status: str = "normal") -> None:
        super().__init__()
        self.setObjectName("status_card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("card_title")
        layout.addWidget(title_label)

        self._value_label = QLabel(value)
        self._set_status(status)
        layout.addWidget(self._value_label)

    def update_value(self, value: str, status: str = "normal") -> None:
        self._value_label.setText(value)
        self._set_status(status)

    def _set_status(self, status: str) -> None:
        style_map = {
            "success": "card_value_success",
            "warning": "card_value_warning",
            "danger": "card_value_danger",
            "normal": "card_value",
        }
        self._value_label.setObjectName(style_map.get(status, "card_value"))
        self._value_label.setStyleSheet("")  # force re-apply


class HomePage(QWidget):
    """Main dashboard page."""

    navigate_to = Signal(str)

    def __init__(
        self,
        config: Config,
        firmware_mgr: FirmwareManager,
        emulator_mgr: EmulatorManager,
        game_lib: GameLibrary,
    ) -> None:
        super().__init__()
        self._config = config
        self._firmware_mgr = firmware_mgr
        self._emulator_mgr = emulator_mgr
        self._game_lib = game_lib
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        title = QLabel("Dashboard")
        title.setObjectName("page_title")
        layout.addWidget(title)

        subtitle = QLabel("Overview of your PS4 emulation setup")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(subtitle)

        # Status cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        self._fw_card = StatusCard("FIRMWARE", "Checking...", "warning")
        self._fw_card.mousePressEvent = lambda _: self.navigate_to.emit("firmware")
        cards_layout.addWidget(self._fw_card, 0, 0)

        self._emu_card = StatusCard("EMULATOR (shadPS4)", "Checking...", "warning")
        self._emu_card.mousePressEvent = lambda _: self.navigate_to.emit("settings")
        cards_layout.addWidget(self._emu_card, 0, 1)

        self._games_card = StatusCard("GAMES", "0 games", "normal")
        self._games_card.mousePressEvent = lambda _: self.navigate_to.emit("library")
        cards_layout.addWidget(self._games_card, 0, 2)

        layout.addLayout(cards_layout)

        # Quick actions section
        section_label = QLabel("Quick Actions")
        section_label.setObjectName("label_section")
        layout.addWidget(section_label)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        btn_firmware = QPushButton("  Install Firmware")
        btn_firmware.clicked.connect(lambda: self.navigate_to.emit("firmware"))
        actions_layout.addWidget(btn_firmware)

        btn_add_games = QPushButton("  Add Games")
        btn_add_games.clicked.connect(lambda: self.navigate_to.emit("library"))
        actions_layout.addWidget(btn_add_games)

        btn_settings = QPushButton("  Settings")
        btn_settings.setObjectName("btn_secondary")
        btn_settings.clicked.connect(lambda: self.navigate_to.emit("settings"))
        actions_layout.addWidget(btn_settings)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Recent games section
        self._recent_section = QLabel("Recent Games")
        self._recent_section.setObjectName("label_section")
        layout.addWidget(self._recent_section)

        self._recent_container = QVBoxLayout()
        self._recent_container.setSpacing(8)
        layout.addLayout(self._recent_container)

        self._no_recent_label = QLabel("No recent games. Add some games to your library to get started!")
        self._no_recent_label.setObjectName("page_subtitle")
        self._no_recent_label.setWordWrap(True)
        self._recent_container.addWidget(self._no_recent_label)

        layout.addStretch()

    def refresh(self) -> None:
        """Refresh all dashboard data."""
        # Firmware status
        fw_info = self._firmware_mgr.get_installed_firmware()
        if fw_info and fw_info.is_valid:
            version = fw_info.version or "Unknown version"
            self._fw_card.update_value(f"v{version} Installed", "success")
        else:
            self._fw_card.update_value("Not Installed", "danger")

        # Emulator status
        if self._emulator_mgr.is_installed():
            self._emu_card.update_value("Detected", "success")
        else:
            self._emu_card.update_value("Not Found", "danger")

        # Games count
        count = self._game_lib.count
        self._games_card.update_value(
            f"{count} game{'s' if count != 1 else ''}",
            "success" if count > 0 else "normal",
        )

        # Recent games
        self._update_recent_games()

    def _update_recent_games(self) -> None:
        recent_ids = self._config.get("recent_games", [])
        has_recent = False

        # Clear old widgets from recent container (except no_recent_label)
        while self._recent_container.count() > 1:
            item = self._recent_container.takeAt(1)
            if item.widget():
                item.widget().deleteLater()

        for game_id in recent_ids[:5]:
            game = self._game_lib.get_game(game_id)
            if game:
                has_recent = True
                row = QFrame()
                row.setObjectName("status_card")
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(12, 8, 12, 8)

                name_label = QLabel(game.title)
                name_label.setStyleSheet("font-weight: bold; font-size: 13px;")
                row_layout.addWidget(name_label)

                id_label = QLabel(game.title_id)
                id_label.setStyleSheet(f"color: #8888aa; font-size: 11px;")
                row_layout.addWidget(id_label)

                row_layout.addStretch()

                if game.last_played:
                    date_str = game.last_played[:10]
                    date_label = QLabel(f"Last played: {date_str}")
                    date_label.setStyleSheet("color: #8888aa; font-size: 11px;")
                    row_layout.addWidget(date_label)

                self._recent_container.addWidget(row)

        self._no_recent_label.setVisible(not has_recent)
