"""Gestion de la configuration de Flux4."""

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = {
    "emulator_path": "",
    "games_directory": "",
    "firmware_path": "",
    "firmware_installed": False,
    "firmware_version": "",
    "gpu_backend": "Vulkan",
    "resolution": "1920x1080",
    "fullscreen": False,
    "log_level": "Info",
    "language": "Français",
    "recent_games": [],
    "theme": "dark",
    "auto_scan_directory": "",
    "check_updates": True,
    "app_version": "1.0.0",
}


class Config:
    """Gère la configuration de l'application stockée en JSON."""

    def __init__(self) -> None:
        self._config_dir = Path.home() / ".ps4-emu-launcher"
        self._config_file = self._config_dir / "config.json"
        self._firmware_dir = self._config_dir / "firmware"
        self._covers_dir = self._config_dir / "covers"
        self._data: dict[str, Any] = {}
        self._ensure_dirs()
        self._load()

    def _ensure_dirs(self) -> None:
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._firmware_dir.mkdir(parents=True, exist_ok=True)
        self._covers_dir.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        if self._config_file.exists():
            try:
                with open(self._config_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._data = {}
        for key, value in DEFAULT_CONFIG.items():
            if key not in self._data:
                self._data[key] = value

    def save(self) -> None:
        with open(self._config_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self.save()

    @property
    def config_dir(self) -> Path:
        return self._config_dir

    @property
    def firmware_dir(self) -> Path:
        return self._firmware_dir

    @property
    def covers_dir(self) -> Path:
        return self._covers_dir

    @property
    def emulator_path(self) -> str:
        return self._data.get("emulator_path", "")

    @emulator_path.setter
    def emulator_path(self, value: str) -> None:
        self.set("emulator_path", value)

    @property
    def games_directory(self) -> str:
        return self._data.get("games_directory", "")

    @games_directory.setter
    def games_directory(self, value: str) -> None:
        self.set("games_directory", value)

    @property
    def firmware_installed(self) -> bool:
        return self._data.get("firmware_installed", False)

    @firmware_installed.setter
    def firmware_installed(self, value: bool) -> None:
        self.set("firmware_installed", value)

    @property
    def firmware_version(self) -> str:
        return self._data.get("firmware_version", "")

    @firmware_version.setter
    def firmware_version(self, value: str) -> None:
        self.set("firmware_version", value)

    @property
    def auto_scan_directory(self) -> str:
        return self._data.get("auto_scan_directory", "")

    @auto_scan_directory.setter
    def auto_scan_directory(self, value: str) -> None:
        self.set("auto_scan_directory", value)

    @property
    def check_updates(self) -> bool:
        return self._data.get("check_updates", True)

    @check_updates.setter
    def check_updates(self, value: bool) -> None:
        self.set("check_updates", value)
