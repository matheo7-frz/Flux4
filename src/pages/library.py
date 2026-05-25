"""Page de la biblioth\u00e8que de jeux : parcourir, ajouter et lancer des jeux PS4."""

import os
from functools import partial

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.config import Config
from src.core.emulator_manager import EmulatorManager
from src.core.game_library import GameEntry, GameLibrary
from src.styles import COLORS


class GameCard(QFrame):
    """Widget carte repr\u00e9sentant un jeu PS4."""

    def __init__(self, game: GameEntry, parent_page: "LibraryPage") -> None:
        super().__init__()
        self.game = game
        self._parent_page = parent_page
        self.setObjectName("game_card")
        self.setFixedSize(180, 260)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Cover image
        cover_frame = QFrame()
        cover_frame.setFixedSize(180, 180)
        cover_frame.setStyleSheet(
            f"background-color: {COLORS['bg_secondary']}; "
            f"border-radius: 12px 12px 0 0;"
        )
        cover_layout = QVBoxLayout(cover_frame)
        cover_layout.setContentsMargins(0, 0, 0, 0)

        cover_label = QLabel()
        cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.game.cover_path and os.path.exists(self.game.cover_path):
            pixmap = QPixmap(self.game.cover_path)
            pixmap = pixmap.scaled(
                178, 178,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            cover_label.setPixmap(pixmap)
        else:
            cover_label.setText("Pas de\njaquette")
            cover_label.setStyleSheet(
                f"color: {COLORS['text_muted']}; font-size: 14px; font-weight: bold;"
            )

        cover_layout.addWidget(cover_label)
        layout.addWidget(cover_frame)

        # Game info
        info_frame = QFrame()
        info_frame.setStyleSheet("background: transparent;")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(10, 6, 10, 8)
        info_layout.setSpacing(2)

        title_label = QLabel(self.game.title)
        title_label.setObjectName("game_title")
        title_label.setWordWrap(True)
        title_label.setMaximumHeight(36)
        info_layout.addWidget(title_label)

        id_text = self.game.title_id or self.game.game_id
        if self.game.region:
            id_text += f" [{self.game.region}]"
        id_label = QLabel(id_text)
        id_label.setObjectName("game_id")
        info_layout.addWidget(id_label)

        layout.addWidget(info_frame)

    def mouseDoubleClickEvent(self, event) -> None:
        self._parent_page.launch_game(self.game)

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)
        menu.setStyleSheet(
            f"QMenu {{ background-color: {COLORS['bg_card']}; border: 1px solid {COLORS['border']}; "
            f"border-radius: 6px; padding: 4px; }}"
            f"QMenu::item {{ padding: 8px 20px; color: {COLORS['text_primary']}; }}"
            f"QMenu::item:selected {{ background-color: {COLORS['accent']}; border-radius: 4px; }}"
        )

        launch_action = menu.addAction("Lancer le jeu")
        launch_action.triggered.connect(lambda: self._parent_page.launch_game(self.game))

        menu.addSeparator()

        fav_text = "Retirer des favoris" if self.game.favorite else "Ajouter aux favoris"
        fav_action = menu.addAction(fav_text)
        fav_action.triggered.connect(lambda: self._parent_page.toggle_favorite(self.game))

        open_folder = menu.addAction("Ouvrir le dossier du jeu")
        open_folder.triggered.connect(lambda: self._parent_page.open_folder(self.game))

        menu.addSeparator()

        remove_action = menu.addAction("Retirer de la biblioth\u00e8que")
        remove_action.triggered.connect(lambda: self._parent_page.remove_game(self.game))

        menu.exec(event.globalPos())


class LibraryPage(QWidget):
    """Page de navigation et gestion de la biblioth\u00e8que de jeux."""

    def __init__(
        self,
        config: Config,
        game_lib: GameLibrary,
        emulator_mgr: EmulatorManager,
    ) -> None:
        super().__init__()
        self._config = config
        self._game_lib = game_lib
        self._emulator_mgr = emulator_mgr
        self._game_cards: list[GameCard] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Biblioth\u00e8que de jeux")
        title.setObjectName("page_title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self._count_label = QLabel("0 jeu")
        self._count_label.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 14px; padding-top: 12px;"
        )
        header_layout.addWidget(self._count_label)

        layout.addLayout(header_layout)

        # Search and action bar
        action_bar = QHBoxLayout()
        action_bar.setSpacing(10)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Rechercher un jeu...")
        self._search_input.setMinimumWidth(250)
        self._search_input.textChanged.connect(self._filter_games)
        action_bar.addWidget(self._search_input)

        action_bar.addStretch()

        btn_add = QPushButton("  Ajouter un jeu")
        btn_add.clicked.connect(self._add_game)
        action_bar.addWidget(btn_add)

        btn_scan = QPushButton("  Scanner un dossier")
        btn_scan.setObjectName("btn_secondary")
        btn_scan.clicked.connect(self._scan_directory)
        action_bar.addWidget(btn_scan)

        layout.addLayout(action_bar)

        # Scrollable game grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._grid_widget = QWidget()
        self._grid_widget.setStyleSheet("background: transparent;")
        self._grid_layout = QGridLayout(self._grid_widget)
        self._grid_layout.setSpacing(15)
        self._grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(self._grid_widget)
        layout.addWidget(scroll)

        # Empty state
        self._empty_label = QLabel(
            "Votre biblioth\u00e8que est vide.\n\n"
            "Cliquez sur 'Ajouter un jeu' pour ajouter un dossier de jeu PS4,\n"
            "ou 'Scanner un dossier' pour trouver automatiquement les jeux."
        )
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 14px; padding: 60px;"
        )
        self._empty_label.setWordWrap(True)
        layout.addWidget(self._empty_label)

    def refresh(self) -> None:
        """Rafra\u00eechir la grille de jeux."""
        self._populate_grid(self._game_lib.games)

    def _populate_grid(self, games: list[GameEntry]) -> None:
        # Clear existing cards
        for card in self._game_cards:
            card.setParent(None)
            card.deleteLater()
        self._game_cards.clear()

        # Remove all items from grid
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._count_label.setText(f"{len(games)} jeu{'x' if len(games) > 1 else ''}")
        self._empty_label.setVisible(len(games) == 0)
        self._grid_widget.setVisible(len(games) > 0)

        cols = 5
        for i, game in enumerate(games):
            card = GameCard(game, self)
            self._game_cards.append(card)
            row = i // cols
            col = i % cols
            self._grid_layout.addWidget(card, row, col)

    def _filter_games(self, text: str) -> None:
        if text.strip():
            filtered = self._game_lib.search(text)
        else:
            filtered = self._game_lib.games
        self._populate_grid(filtered)

    def _add_game(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "S\u00e9lectionner le dossier du jeu PS4",
            self._config.games_directory or "",
        )
        if not directory:
            return

        game = self._game_lib.add_game(directory)
        if game:
            QMessageBox.information(
                self,
                "Jeu ajout\u00e9",
                f"'{game.title}' a \u00e9t\u00e9 ajout\u00e9 \u00e0 votre biblioth\u00e8que !",
            )
            self.refresh()
        else:
            QMessageBox.warning(
                self,
                "Dossier de jeu invalide",
                "Le dossier s\u00e9lectionn\u00e9 ne semble pas \u00eatre un dump de jeu PS4 valide.\n\n"
                "Un dossier de jeu PS4 valide doit contenir un fichier EBOOT.BIN\n"
                "et/ou un fichier de m\u00e9tadonn\u00e9es sce_sys/param.sfo.",
            )

    def _scan_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "S\u00e9lectionner le dossier \u00e0 scanner",
            self._config.games_directory or "",
        )
        if not directory:
            return

        added = self._game_lib.scan_directory(directory)
        if added:
            names = ", ".join(g.title for g in added[:5])
            extra = f" et {len(added) - 5} autres" if len(added) > 5 else ""
            QMessageBox.information(
                self,
                "Scan termin\u00e9",
                f"{len(added)} jeu(x) trouv\u00e9(s) : {names}{extra}",
            )
            self._config.games_directory = directory
            self.refresh()
        else:
            QMessageBox.information(
                self,
                "Scan termin\u00e9",
                "Aucun nouveau jeu PS4 trouv\u00e9 dans le dossier s\u00e9lectionn\u00e9.",
            )

    def launch_game(self, game: GameEntry) -> None:
        if not self._config.firmware_installed:
            QMessageBox.warning(
                self,
                "Firmware obligatoire",
                "Le firmware PS4 n'est pas install\u00e9.\n\n"
                "Vous devez d'abord aller dans la page Firmware et importer un fichier firmware.\n"
                "Sans firmware, il est impossible de lancer un jeu.",
            )
            return

        if not self._emulator_mgr.is_installed():
            QMessageBox.warning(
                self,
                "\u00c9mulateur non trouv\u00e9",
                "shadPS4 n'est pas install\u00e9 ou n'est pas configur\u00e9.\n\n"
                "Allez dans les Param\u00e8tres et d\u00e9finissez le chemin de l'\u00e9mulateur.",
            )
            return

        self._game_lib.update_last_played(game.game_id)
        process = self._emulator_mgr.launch_game(game.path)
        if not process:
            QMessageBox.critical(
                self,
                "\u00c9chec du lancement",
                f"Impossible de lancer '{game.title}'.\n\n"
                "V\u00e9rifiez que les fichiers du jeu sont valides et que l'\u00e9mulateur est bien configur\u00e9.",
            )

    def toggle_favorite(self, game: GameEntry) -> None:
        self._game_lib.toggle_favorite(game.game_id)
        self.refresh()

    def remove_game(self, game: GameEntry) -> None:
        reply = QMessageBox.question(
            self,
            "Retirer le jeu",
            f"Retirer '{game.title}' de la biblioth\u00e8que ?\n\n"
            "(Les fichiers du jeu ne seront PAS supprim\u00e9s du disque.)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._game_lib.remove_game(game.game_id)
            self.refresh()

    def open_folder(self, game: GameEntry) -> None:
        import subprocess
        import sys

        path = game.path
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
