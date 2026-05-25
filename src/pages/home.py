"""Page d'accueil style PS4 : affiche les jeux et le statut du systeme."""

import webbrowser

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
from src.core.updater import UpdateInfo
from src.styles import COLORS


class StatusCard(QFrame):
    """Widget de carte de statut compact."""

    def __init__(self, title: str, value: str, status: str = "normal") -> None:
        super().__init__()
        self.setObjectName("status_card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(14, 12, 14, 12)

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
        self._value_label.setStyleSheet("")


class HomePage(QWidget):
    """Page d'accueil avec vue d'ensemble PS4."""

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
        self._update_info: UpdateInfo | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(10)

        # Banniere de mise a jour
        self._update_banner = QFrame()
        self._update_banner.setVisible(False)
        self._update_banner.setStyleSheet(
            f"background-color: rgba(46, 204, 113, 0.15); "
            f"border: 1px solid {COLORS['success']}; "
            f"border-radius: 6px; padding: 8px;"
        )
        banner_layout = QHBoxLayout(self._update_banner)
        banner_layout.setContentsMargins(10, 6, 10, 6)

        self._update_label = QLabel("")
        self._update_label.setStyleSheet(
            f"color: {COLORS['success']}; font-weight: bold; font-size: 12px;"
        )
        banner_layout.addWidget(self._update_label)

        banner_layout.addStretch()

        self._update_dl_btn = QPushButton("T\u00e9l\u00e9charger")
        self._update_dl_btn.setStyleSheet(
            f"background-color: {COLORS['success']}; color: #000; "
            f"font-weight: bold; padding: 5px 14px; border-radius: 4px;"
        )
        banner_layout.addWidget(self._update_dl_btn)

        layout.addWidget(self._update_banner)

        # Cartes de statut en ligne
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self._fw_card = StatusCard("FIRMWARE", "V\u00e9rification...", "warning")
        self._fw_card.mousePressEvent = lambda _: self.navigate_to.emit("settings")
        cards_layout.addWidget(self._fw_card)

        self._emu_card = StatusCard("\u00c9MULATEUR", "V\u00e9rification...", "warning")
        self._emu_card.mousePressEvent = lambda _: self.navigate_to.emit("settings")
        cards_layout.addWidget(self._emu_card)

        self._games_card = StatusCard("JEUX", "0 jeu", "normal")
        self._games_card.mousePressEvent = lambda _: self.navigate_to.emit("library")
        cards_layout.addWidget(self._games_card)

        layout.addLayout(cards_layout)

        # Actions rapides
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        btn_library = QPushButton("  Biblioth\u00e8que")
        btn_library.clicked.connect(lambda: self.navigate_to.emit("library"))
        actions_layout.addWidget(btn_library)

        btn_settings = QPushButton("  Param\u00e8tres")
        btn_settings.setObjectName("btn_secondary")
        btn_settings.clicked.connect(lambda: self.navigate_to.emit("settings"))
        actions_layout.addWidget(btn_settings)

        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Jeux recents
        self._recent_section = QLabel("Jeux r\u00e9cents")
        self._recent_section.setObjectName("label_section")
        layout.addWidget(self._recent_section)

        self._recent_container = QVBoxLayout()
        self._recent_container.setSpacing(6)
        layout.addLayout(self._recent_container)

        self._no_recent_label = QLabel(
            "Aucun jeu r\u00e9cent. Ajoutez des jeux dans la Biblioth\u00e8que pour commencer !"
        )
        self._no_recent_label.setObjectName("page_subtitle")
        self._no_recent_label.setWordWrap(True)
        self._recent_container.addWidget(self._no_recent_label)

        layout.addStretch()

    def set_update_info(self, info: UpdateInfo) -> None:
        """Afficher la banniere de mise a jour."""
        self._update_info = info
        self._update_banner.setVisible(True)
        self._update_label.setText(
            f"Nouvelle version v{info.latest_version} disponible ! "
            f"(vous avez v{info.current_version})"
        )
        self._update_dl_btn.clicked.connect(
            lambda: webbrowser.open(info.release_url)
        )

    def refresh(self) -> None:
        """Rafra\u00eechir toutes les donnees."""
        fw_info = self._firmware_mgr.get_installed_firmware()
        if fw_info and fw_info.is_valid:
            version = fw_info.version or "?"
            self._fw_card.update_value(f"v{version}", "success")
        else:
            self._fw_card.update_value("Non install\u00e9", "danger")

        if self._emulator_mgr.is_installed():
            self._emu_card.update_value("D\u00e9tect\u00e9", "success")
        else:
            self._emu_card.update_value("Non trouv\u00e9", "danger")

        count = self._game_lib.count
        self._games_card.update_value(
            f"{count} jeu{'x' if count > 1 else ''}",
            "success" if count > 0 else "normal",
        )

        self._update_recent_games()

    def _update_recent_games(self) -> None:
        recent_ids = self._config.get("recent_games", [])
        has_recent = False

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
                row_layout.setContentsMargins(10, 6, 10, 6)

                name_label = QLabel(game.title)
                name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
                row_layout.addWidget(name_label)

                id_label = QLabel(game.title_id)
                id_label.setStyleSheet("color: #8888aa; font-size: 10px;")
                row_layout.addWidget(id_label)

                row_layout.addStretch()

                if game.last_played:
                    date_str = game.last_played[:10]
                    date_label = QLabel(f"Derni\u00e8re partie : {date_str}")
                    date_label.setStyleSheet("color: #8888aa; font-size: 10px;")
                    row_layout.addWidget(date_label)

                self._recent_container.addWidget(row)

        self._no_recent_label.setVisible(not has_recent)
