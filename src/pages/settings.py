"""Page des param\u00e8tres : configurer le chemin de l'\u00e9mulateur, graphismes et pr\u00e9f\u00e9rences."""

import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.config import Config
from src.core.emulator_manager import EmulatorManager, SHADPS4_RELEASES_URL
from src.styles import COLORS


class SettingsPage(QWidget):
    """Page de configuration et param\u00e8tres de l'application."""

    def __init__(self, config: Config, emulator_mgr: EmulatorManager) -> None:
        super().__init__()
        self._config = config
        self._emulator_mgr = emulator_mgr
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        title = QLabel("Param\u00e8tres")
        title.setObjectName("page_title")
        layout.addWidget(title)

        subtitle = QLabel("Configurez votre environnement d'\u00e9mulation PS4")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(subtitle)

        # Emulator section
        self._add_section(layout, "\u00c9mulateur (shadPS4)")

        # Emulator status
        self._emu_status = QLabel("V\u00e9rification...")
        self._emu_status.setStyleSheet(f"color: {COLORS['warning']}; font-weight: bold;")
        layout.addWidget(self._emu_status)

        # Emulator path
        self._add_field_label(layout, "Chemin de l'\u00e9mulateur")
        path_layout = QHBoxLayout()
        self._emu_path_input = QLineEdit()
        self._emu_path_input.setPlaceholderText("Chemin vers l'ex\u00e9cutable shadPS4...")
        self._emu_path_input.setReadOnly(True)
        path_layout.addWidget(self._emu_path_input)

        btn_browse_emu = QPushButton("Parcourir")
        btn_browse_emu.setObjectName("btn_secondary")
        btn_browse_emu.setFixedWidth(100)
        btn_browse_emu.clicked.connect(self._browse_emulator)
        path_layout.addWidget(btn_browse_emu)

        btn_detect = QPushButton("D\u00e9tecter")
        btn_detect.setObjectName("btn_secondary")
        btn_detect.setFixedWidth(100)
        btn_detect.clicked.connect(self._auto_detect)
        path_layout.addWidget(btn_detect)

        layout.addLayout(path_layout)

        # Download button
        dl_layout = QHBoxLayout()
        btn_download = QPushButton("  T\u00e9l\u00e9charger shadPS4 depuis GitHub")
        btn_download.setObjectName("btn_secondary")
        btn_download.clicked.connect(self._open_download_page)
        dl_layout.addWidget(btn_download)
        dl_layout.addStretch()
        layout.addLayout(dl_layout)

        self._add_separator(layout)

        # Games directory
        self._add_section(layout, "R\u00e9pertoire des jeux")
        self._add_field_label(layout, "Dossier par d\u00e9faut pour scanner les jeux PS4")

        games_layout = QHBoxLayout()
        self._games_dir_input = QLineEdit()
        self._games_dir_input.setPlaceholderText("Dossier par d\u00e9faut pour les jeux...")
        self._games_dir_input.setReadOnly(True)
        games_layout.addWidget(self._games_dir_input)

        btn_browse_games = QPushButton("Parcourir")
        btn_browse_games.setObjectName("btn_secondary")
        btn_browse_games.setFixedWidth(100)
        btn_browse_games.clicked.connect(self._browse_games_dir)
        games_layout.addWidget(btn_browse_games)

        layout.addLayout(games_layout)

        self._add_field_label(layout, "Dossier de scan automatique (les jeux sont d\u00e9tect\u00e9s au d\u00e9marrage)")

        auto_scan_layout = QHBoxLayout()
        self._auto_scan_input = QLineEdit()
        self._auto_scan_input.setPlaceholderText("Dossier \u00e0 scanner automatiquement au d\u00e9marrage...")
        self._auto_scan_input.setReadOnly(True)
        auto_scan_layout.addWidget(self._auto_scan_input)

        btn_browse_auto = QPushButton("Parcourir")
        btn_browse_auto.setObjectName("btn_secondary")
        btn_browse_auto.setFixedWidth(100)
        btn_browse_auto.clicked.connect(self._browse_auto_scan_dir)
        auto_scan_layout.addWidget(btn_browse_auto)

        btn_clear_auto = QPushButton("Effacer")
        btn_clear_auto.setObjectName("btn_secondary")
        btn_clear_auto.setFixedWidth(100)
        btn_clear_auto.clicked.connect(self._clear_auto_scan_dir)
        auto_scan_layout.addWidget(btn_clear_auto)

        layout.addLayout(auto_scan_layout)

        self._add_separator(layout)

        # Graphics settings
        self._add_section(layout, "Graphismes")

        self._add_field_label(layout, "Moteur GPU")
        self._gpu_combo = QComboBox()
        self._gpu_combo.addItems(["Vulkan", "OpenGL"])
        self._gpu_combo.currentTextChanged.connect(
            lambda v: self._config.set("gpu_backend", v)
        )
        layout.addWidget(self._gpu_combo)

        self._add_field_label(layout, "R\u00e9solution")
        self._res_combo = QComboBox()
        self._res_combo.addItems([
            "1280x720", "1920x1080", "2560x1440", "3840x2160",
        ])
        self._res_combo.currentTextChanged.connect(
            lambda v: self._config.set("resolution", v)
        )
        layout.addWidget(self._res_combo)

        self._fullscreen_check = QCheckBox("Lancer les jeux en plein \u00e9cran")
        self._fullscreen_check.stateChanged.connect(
            lambda s: self._config.set("fullscreen", s == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self._fullscreen_check)

        self._add_separator(layout)

        # Updates section
        self._add_section(layout, "Mises \u00e0 jour")

        self._check_updates_check = QCheckBox("V\u00e9rifier les mises \u00e0 jour au d\u00e9marrage")
        self._check_updates_check.stateChanged.connect(
            lambda s: self._config.set("check_updates", s == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self._check_updates_check)

        self._add_separator(layout)

        # Advanced
        self._add_section(layout, "Avanc\u00e9")

        self._add_field_label(layout, "Niveau de log")
        self._log_combo = QComboBox()
        self._log_combo.addItems(["Trace", "Debug", "Info", "Warning", "Error"])
        self._log_combo.currentTextChanged.connect(
            lambda v: self._config.set("log_level", v)
        )
        layout.addWidget(self._log_combo)

        self._add_separator(layout)

        # Reset
        btn_reset = QPushButton("  R\u00e9initialiser tous les param\u00e8tres")
        btn_reset.setObjectName("btn_danger")
        btn_reset.clicked.connect(self._reset_settings)
        layout.addWidget(btn_reset)

        layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def refresh(self) -> None:
        """Rafra\u00eechir les valeurs depuis la configuration."""
        emu_path = self._emulator_mgr.detect_emulator()
        if emu_path:
            self._emu_path_input.setText(emu_path)
            self._emu_status.setText("shadPS4 d\u00e9tect\u00e9")
            self._emu_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
        else:
            self._emu_path_input.setText("")
            self._emu_status.setText("shadPS4 non trouv\u00e9 - D\u00e9finissez le chemin ou t\u00e9l\u00e9chargez-le")
            self._emu_status.setStyleSheet(f"color: {COLORS['danger']}; font-weight: bold;")

        self._games_dir_input.setText(self._config.games_directory)
        self._auto_scan_input.setText(self._config.auto_scan_directory)

        gpu = self._config.get("gpu_backend", "Vulkan")
        idx = self._gpu_combo.findText(gpu)
        if idx >= 0:
            self._gpu_combo.setCurrentIndex(idx)

        res = self._config.get("resolution", "1920x1080")
        idx = self._res_combo.findText(res)
        if idx >= 0:
            self._res_combo.setCurrentIndex(idx)

        self._fullscreen_check.setChecked(self._config.get("fullscreen", False))
        self._check_updates_check.setChecked(self._config.get("check_updates", True))

        log_level = self._config.get("log_level", "Info")
        idx = self._log_combo.findText(log_level)
        if idx >= 0:
            self._log_combo.setCurrentIndex(idx)

    def _browse_emulator(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "S\u00e9lectionner l'ex\u00e9cutable shadPS4",
            "",
            "Fichiers ex\u00e9cutables (*.exe *.AppImage shadps4 shadPS4);;Tous les fichiers (*)",
        )
        if filepath:
            if self._emulator_mgr.set_emulator_path(filepath):
                self._emu_path_input.setText(filepath)
                self._emu_status.setText("shadPS4 configur\u00e9")
                self._emu_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
            else:
                QMessageBox.warning(self, "Chemin invalide", "Le fichier s\u00e9lectionn\u00e9 n'existe pas.")

    def _auto_detect(self) -> None:
        path = self._emulator_mgr.detect_emulator()
        if path:
            self._emu_path_input.setText(path)
            self._emu_status.setText("shadPS4 d\u00e9tect\u00e9")
            self._emu_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
            QMessageBox.information(
                self, "\u00c9mulateur trouv\u00e9", f"shadPS4 d\u00e9tect\u00e9 \u00e0 :\n{path}"
            )
        else:
            QMessageBox.information(
                self,
                "Non trouv\u00e9",
                "shadPS4 n'a pas \u00e9t\u00e9 trouv\u00e9 sur votre syst\u00e8me.\n\n"
                "Veuillez le t\u00e9l\u00e9charger depuis GitHub ou d\u00e9finir le chemin manuellement.",
            )

    def _browse_auto_scan_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "S\u00e9lectionner le dossier de scan automatique",
            self._config.auto_scan_directory or self._config.games_directory or "",
        )
        if directory:
            self._config.auto_scan_directory = directory
            self._auto_scan_input.setText(directory)

    def _clear_auto_scan_dir(self) -> None:
        self._config.auto_scan_directory = ""
        self._auto_scan_input.setText("")

    def _browse_games_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "S\u00e9lectionner le r\u00e9pertoire des jeux",
            self._config.games_directory or "",
        )
        if directory:
            self._config.games_directory = directory
            self._games_dir_input.setText(directory)

    def _open_download_page(self) -> None:
        webbrowser.open(SHADPS4_RELEASES_URL)

    def _reset_settings(self) -> None:
        reply = QMessageBox.question(
            self,
            "R\u00e9initialiser les param\u00e8tres",
            "R\u00e9initialiser tous les param\u00e8tres \u00e0 leurs valeurs par d\u00e9faut ?\n\n"
            "Cela ne supprimera pas votre firmware ni votre biblioth\u00e8que de jeux.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            from src.core.config import DEFAULT_CONFIG
            for key, value in DEFAULT_CONFIG.items():
                if key not in ("firmware_path", "firmware_installed", "firmware_version", "recent_games"):
                    self._config.set(key, value)
            self.refresh()

    @staticmethod
    def _add_section(layout: QVBoxLayout, text: str) -> None:
        label = QLabel(text)
        label.setObjectName("label_section")
        layout.addWidget(label)

    @staticmethod
    def _add_field_label(layout: QVBoxLayout, text: str) -> None:
        label = QLabel(text)
        label.setObjectName("label_field")
        layout.addWidget(label)

    @staticmethod
    def _add_separator(layout: QVBoxLayout) -> None:
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)
