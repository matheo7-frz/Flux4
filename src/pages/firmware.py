"""Page de gestion du firmware : importer, valider et gerer le firmware PS4."""

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
    """Page de gestion du firmware PS4."""

    def __init__(self, config: Config, firmware_mgr: FirmwareManager) -> None:
        super().__init__()
        self._config = config
        self._firmware_mgr = firmware_mgr
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        title = QLabel("Gestion du Firmware")
        title.setObjectName("page_title")
        layout.addWidget(title)

        subtitle = QLabel(
            "Importez et g\u00e9rez votre firmware PS4 (PS4UPDATE.PUP). "
            "Le firmware est obligatoire pour lancer les jeux avec shadPS4."
        )
        subtitle.setObjectName("page_subtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Current firmware status card
        self._status_card = QFrame()
        self._status_card.setObjectName("status_card")
        status_layout = QVBoxLayout(self._status_card)
        status_layout.setSpacing(8)

        status_header = QLabel("FIRMWARE ACTUEL")
        status_header.setObjectName("card_title")
        status_layout.addWidget(status_header)

        self._status_label = QLabel("Non install\u00e9")
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

        self._btn_import = QPushButton("  Importer le Firmware (.PUP)")
        self._btn_import.setMinimumHeight(44)
        self._btn_import.clicked.connect(self._import_firmware)
        btn_layout.addWidget(self._btn_import)

        self._btn_uninstall = QPushButton("  D\u00e9sinstaller le Firmware")
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

        help_title = QLabel("Comment obtenir le Firmware PS4")
        help_title.setObjectName("label_section")
        layout.addWidget(help_title)

        help_text = QLabel(
            "1. Vous avez besoin d'un fichier PS4UPDATE.PUP (le fichier officiel de mise \u00e0 jour syst\u00e8me PS4).\n\n"
            "2. Ces fichiers peuvent \u00eatre obtenus depuis votre propre console PS4 ou depuis le site officiel "
            "de PlayStation pour la r\u00e9cup\u00e9ration.\n\n"
            "3. Le fichier fait g\u00e9n\u00e9ralement entre 500 Mo et 1,1 Go selon la version.\n\n"
            "4. Cliquez sur 'Importer le Firmware' ci-dessus et s\u00e9lectionnez votre fichier .PUP. "
            "Le lanceur le validera et l'installera automatiquement.\n\n"
            "5. shadPS4 fonctionne mieux avec les versions de firmware 1.00 \u00e0 5.05, "
            "bien que la compatibilit\u00e9 varie selon les jeux."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet(
            f"color: {COLORS['text_secondary']}; font-size: 12px; line-height: 1.6;"
        )
        layout.addWidget(help_text)

        layout.addStretch()

    def refresh(self) -> None:
        """Rafra\u00eechir l'affichage du statut du firmware."""
        fw_info = self._firmware_mgr.get_installed_firmware()
        if fw_info and fw_info.is_valid:
            version = fw_info.version or "Inconnue"
            self._status_label.setText(f"v{version} - Install\u00e9")
            self._status_label.setObjectName("card_value_success")
            self._status_label.setStyleSheet(
                f"font-size: 20px; font-weight: bold; color: {COLORS['success']};"
            )
            self._version_label.setText(f"Version : {version}")
            self._size_label.setText(f"Taille : {fw_info.size_display}")
            self._hash_label.setText(f"SHA-256 : {fw_info.sha256[:32]}...")
            self._path_label.setText(f"Chemin : {fw_info.path}")
            self._btn_uninstall.setEnabled(True)
        else:
            self._status_label.setText("Non install\u00e9")
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
            "S\u00e9lectionner le fichier Firmware PS4",
            "",
            "Firmware PS4 (*.PUP *.pup);;Tous les fichiers (*)",
        )
        if not filepath:
            return

        info = self._firmware_mgr.import_firmware(filepath)
        if info.is_valid:
            version = info.version or "Inconnue"
            QMessageBox.information(
                self,
                "Firmware install\u00e9",
                f"Le firmware PS4 v{version} a \u00e9t\u00e9 install\u00e9 avec succ\u00e8s !\n\n"
                f"Fichier : {info.filename}\n"
                f"Taille : {info.size_display}",
            )
        else:
            QMessageBox.warning(
                self,
                "\u00c9chec de l'importation",
                f"Le fichier s\u00e9lectionn\u00e9 n'est pas un firmware PS4 valide.\n\n"
                f"Erreur : {info.error}",
            )

        self.refresh()

    def _uninstall_firmware(self) -> None:
        reply = QMessageBox.question(
            self,
            "Confirmer la d\u00e9sinstallation",
            "\u00cates-vous s\u00fbr de vouloir d\u00e9sinstaller le firmware PS4 ?\n\n"
            "Les jeux ne fonctionneront pas sans firmware install\u00e9.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._firmware_mgr.uninstall_firmware()
            self.refresh()
