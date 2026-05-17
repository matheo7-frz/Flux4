"""Firmware management page: import, validate, and manage PS4 firmware."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.config import Config
from src.core.firmware_manager import FirmwareManager
from src.styles import COLORS


class FirmwarePage(QWidget):
    """Page for managing PS4 firmware."""

    def __init__(self, config: Config, firmware_mgr: FirmwareManager) -> None:
        super().__init__()
        self._config = config
        self._firmware_mgr = firmware_mgr
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        title = QLabel("Firmware Management")
        title.setObjectName("page_title")
        layout.addWidget(title)

        subtitle = QLabel(
            "Import and manage your PS4 firmware (PS4UPDATE.PUP). "
            "The firmware is required by shadPS4 to run games."
        )
        subtitle.setObjectName("page_subtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Current firmware status card
        self._status_card = QFrame()
        self._status_card.setObjectName("status_card")
        status_layout = QVBoxLayout(self._status_card)
        status_layout.setSpacing(8)

        status_header = QLabel("CURRENT FIRMWARE")
        status_header.setObjectName("card_title")
        status_layout.addWidget(status_header)

        self._status_label = QLabel("Not installed")
        self._status_label.setObjectName("card_value_danger")
        self._status_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        status_layout.addWidget(self._status_label)

        self._info_container = QVBoxLayout()
        self._info_container.setSpacing(4)
        status_layout.addLayout(self._info_container)

        self._version_label = QLabel("")
        self._version_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        self._info_container.addWidget(self._version_label)

        self._size_label = QLabel("")
        self._size_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px;")
        self._info_container.addWidget(self._size_label)

        self._hash_label = QLabel("")
        self._hash_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        self._hash_label.setWordWrap(True)
        self._info_container.addWidget(self._hash_label)

        self._path_label = QLabel("")
        self._path_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px;")
        self._path_label.setWordWrap(True)
        self._info_container.addWidget(self._path_label)

        layout.addWidget(self._status_card)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self._btn_import = QPushButton("  Import Firmware (.PUP)")
        self._btn_import.setMinimumHeight(44)
        self._btn_import.clicked.connect(self._import_firmware)
        btn_layout.addWidget(self._btn_import)

        self._btn_uninstall = QPushButton("  Uninstall Firmware")
        self._btn_uninstall.setObjectName("btn_danger")
        self._btn_uninstall.setMinimumHeight(44)
        self._btn_uninstall.clicked.connect(self._uninstall_firmware)
        btn_layout.addWidget(self._btn_uninstall)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Help section
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)

        help_title = QLabel("How to get PS4 Firmware")
        help_title.setObjectName("label_section")
        layout.addWidget(help_title)

        help_text = QLabel(
            "1. You need a PS4UPDATE.PUP file (the official PS4 system software update file).\n\n"
            "2. These files can be obtained from your own PS4 console or from Sony's official "
            "PlayStation website for recovery purposes.\n\n"
            "3. The file is typically around 500 MB to 1.1 GB depending on the version.\n\n"
            "4. Click 'Import Firmware' above and select your .PUP file. "
            "The launcher will validate and install it automatically.\n\n"
            "5. shadPS4 currently works best with firmware versions 1.00 to 5.05, "
            "though compatibility varies by game."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 12px; line-height: 1.6;"
        )
        layout.addWidget(help_text)

        layout.addStretch()

    def refresh(self) -> None:
        """Refresh firmware status display."""
        fw_info = self._firmware_mgr.get_installed_firmware()
        if fw_info and fw_info.is_valid:
            version = fw_info.version or "Unknown"
            self._status_label.setText(f"v{version} - Installed")
            self._status_label.setObjectName("card_value_success")
            self._status_label.setStyleSheet(
                f"font-size: 20px; font-weight: bold; color: {COLORS['success']};"
            )
            self._version_label.setText(f"Version: {version}")
            self._size_label.setText(f"Size: {fw_info.size_display}")
            self._hash_label.setText(f"SHA-256: {fw_info.sha256[:32]}...")
            self._path_label.setText(f"Path: {fw_info.path}")
            self._btn_uninstall.setEnabled(True)
        else:
            self._status_label.setText("Not Installed")
            self._status_label.setObjectName("card_value_danger")
            self._status_label.setStyleSheet(
                f"font-size: 20px; font-weight: bold; color: {COLORS['danger']};"
            )
            self._version_label.setText("")
            self._size_label.setText("")
            self._hash_label.setText("")
            self._path_label.setText("")
            self._btn_uninstall.setEnabled(False)

    def _import_firmware(self) -> None:
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select PS4 Firmware File",
            "",
            "PS4 Firmware (*.PUP *.pup);;All Files (*)",
        )
        if not filepath:
            return

        info = self._firmware_mgr.import_firmware(filepath)
        if info.is_valid:
            version = info.version or "Unknown"
            QMessageBox.information(
                self,
                "Firmware Installed",
                f"PS4 firmware v{version} has been successfully installed!\n\n"
                f"File: {info.filename}\n"
                f"Size: {info.size_display}",
            )
        else:
            QMessageBox.warning(
                self,
                "Firmware Import Failed",
                f"The selected file is not a valid PS4 firmware.\n\n"
                f"Error: {info.error}",
            )

        self.refresh()

    def _uninstall_firmware(self) -> None:
        reply = QMessageBox.question(
            self,
            "Confirm Uninstall",
            "Are you sure you want to uninstall the PS4 firmware?\n\n"
            "Games will not work without firmware installed.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._firmware_mgr.uninstall_firmware()
            self.refresh()
