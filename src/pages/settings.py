"""Settings page: configure emulator path, graphics, and preferences."""

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
    """Application settings and configuration page."""

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

        title = QLabel("Settings")
        title.setObjectName("page_title")
        layout.addWidget(title)

        subtitle = QLabel("Configure your PS4 emulation environment")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(subtitle)

        # Emulator section
        self._add_section(layout, "Emulator (shadPS4)")

        # Emulator status
        self._emu_status = QLabel("Checking...")
        self._emu_status.setStyleSheet(f"color: {COLORS['warning']}; font-weight: bold;")
        layout.addWidget(self._emu_status)

        # Emulator path
        self._add_field_label(layout, "Emulator Path")
        path_layout = QHBoxLayout()
        self._emu_path_input = QLineEdit()
        self._emu_path_input.setPlaceholderText("Path to shadPS4 executable...")
        self._emu_path_input.setReadOnly(True)
        path_layout.addWidget(self._emu_path_input)

        btn_browse_emu = QPushButton("Browse")
        btn_browse_emu.setObjectName("btn_secondary")
        btn_browse_emu.setFixedWidth(100)
        btn_browse_emu.clicked.connect(self._browse_emulator)
        path_layout.addWidget(btn_browse_emu)

        btn_detect = QPushButton("Auto-detect")
        btn_detect.setObjectName("btn_secondary")
        btn_detect.setFixedWidth(100)
        btn_detect.clicked.connect(self._auto_detect)
        path_layout.addWidget(btn_detect)

        layout.addLayout(path_layout)

        # Download button
        dl_layout = QHBoxLayout()
        btn_download = QPushButton("  Download shadPS4 from GitHub")
        btn_download.setObjectName("btn_secondary")
        btn_download.clicked.connect(self._open_download_page)
        dl_layout.addWidget(btn_download)
        dl_layout.addStretch()
        layout.addLayout(dl_layout)

        self._add_separator(layout)

        # Games directory
        self._add_section(layout, "Games Directory")
        self._add_field_label(layout, "Default scan directory for PS4 games")

        games_layout = QHBoxLayout()
        self._games_dir_input = QLineEdit()
        self._games_dir_input.setPlaceholderText("Default directory to scan for games...")
        self._games_dir_input.setReadOnly(True)
        games_layout.addWidget(self._games_dir_input)

        btn_browse_games = QPushButton("Browse")
        btn_browse_games.setObjectName("btn_secondary")
        btn_browse_games.setFixedWidth(100)
        btn_browse_games.clicked.connect(self._browse_games_dir)
        games_layout.addWidget(btn_browse_games)

        layout.addLayout(games_layout)

        self._add_separator(layout)

        # Graphics settings
        self._add_section(layout, "Graphics")

        self._add_field_label(layout, "GPU Backend")
        self._gpu_combo = QComboBox()
        self._gpu_combo.addItems(["Vulkan", "OpenGL"])
        self._gpu_combo.currentTextChanged.connect(
            lambda v: self._config.set("gpu_backend", v)
        )
        layout.addWidget(self._gpu_combo)

        self._add_field_label(layout, "Resolution")
        self._res_combo = QComboBox()
        self._res_combo.addItems([
            "1280x720", "1920x1080", "2560x1440", "3840x2160",
        ])
        self._res_combo.currentTextChanged.connect(
            lambda v: self._config.set("resolution", v)
        )
        layout.addWidget(self._res_combo)

        self._fullscreen_check = QCheckBox("Launch games in fullscreen")
        self._fullscreen_check.stateChanged.connect(
            lambda s: self._config.set("fullscreen", s == Qt.CheckState.Checked.value)
        )
        layout.addWidget(self._fullscreen_check)

        self._add_separator(layout)

        # Advanced
        self._add_section(layout, "Advanced")

        self._add_field_label(layout, "Log Level")
        self._log_combo = QComboBox()
        self._log_combo.addItems(["Trace", "Debug", "Info", "Warning", "Error"])
        self._log_combo.currentTextChanged.connect(
            lambda v: self._config.set("log_level", v)
        )
        layout.addWidget(self._log_combo)

        self._add_separator(layout)

        # Reset
        btn_reset = QPushButton("  Reset All Settings to Default")
        btn_reset.setObjectName("btn_danger")
        btn_reset.clicked.connect(self._reset_settings)
        layout.addWidget(btn_reset)

        layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def refresh(self) -> None:
        """Refresh settings values from config."""
        emu_path = self._emulator_mgr.detect_emulator()
        if emu_path:
            self._emu_path_input.setText(emu_path)
            self._emu_status.setText("shadPS4 detected")
            self._emu_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
        else:
            self._emu_path_input.setText("")
            self._emu_status.setText("shadPS4 not found - Please set the path or download it")
            self._emu_status.setStyleSheet(f"color: {COLORS['danger']}; font-weight: bold;")

        self._games_dir_input.setText(self._config.games_directory)

        gpu = self._config.get("gpu_backend", "Vulkan")
        idx = self._gpu_combo.findText(gpu)
        if idx >= 0:
            self._gpu_combo.setCurrentIndex(idx)

        res = self._config.get("resolution", "1920x1080")
        idx = self._res_combo.findText(res)
        if idx >= 0:
            self._res_combo.setCurrentIndex(idx)

        self._fullscreen_check.setChecked(self._config.get("fullscreen", False))

        log_level = self._config.get("log_level", "Info")
        idx = self._log_combo.findText(log_level)
        if idx >= 0:
            self._log_combo.setCurrentIndex(idx)

    def _browse_emulator(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select shadPS4 Executable",
            "",
            "Executable Files (*.exe *.AppImage shadps4 shadPS4);;All Files (*)",
        )
        if filepath:
            if self._emulator_mgr.set_emulator_path(filepath):
                self._emu_path_input.setText(filepath)
                self._emu_status.setText("shadPS4 configured")
                self._emu_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
            else:
                QMessageBox.warning(self, "Invalid Path", "The selected file does not exist.")

    def _auto_detect(self) -> None:
        path = self._emulator_mgr.detect_emulator()
        if path:
            self._emu_path_input.setText(path)
            self._emu_status.setText("shadPS4 detected")
            self._emu_status.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold;")
            QMessageBox.information(
                self, "Emulator Found", f"shadPS4 detected at:\n{path}"
            )
        else:
            QMessageBox.information(
                self,
                "Not Found",
                "shadPS4 was not found on your system.\n\n"
                "Please download it from GitHub or manually set the path.",
            )

    def _browse_games_dir(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Games Directory",
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
            "Reset Settings",
            "Reset all settings to their default values?\n\n"
            "This will not remove your firmware or game library.",
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
