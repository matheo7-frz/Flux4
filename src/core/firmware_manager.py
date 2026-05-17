"""PS4 Firmware management: import, validate, and track firmware files."""

import hashlib
import os
import shutil
import struct
from dataclasses import dataclass
from pathlib import Path

from src.core.config import Config


PUP_MAGIC = b"\x4F\x15\x3D\x1D"
KNOWN_VERSIONS = {
    "1.00", "1.01", "1.50", "1.51", "1.52", "1.70", "1.71", "1.76",
    "2.00", "2.01", "2.02", "2.03", "2.04", "2.50", "2.51", "2.55", "2.57",
    "3.00", "3.01", "3.10", "3.11", "3.15", "3.50", "3.55", "3.70",
    "4.00", "4.01", "4.05", "4.06", "4.07", "4.50", "4.55", "4.70", "4.71", "4.72", "4.73", "4.74",
    "5.00", "5.01", "5.03", "5.05", "5.07", "5.50", "5.53", "5.55", "5.56",
    "6.00", "6.02", "6.20", "6.50", "6.51", "6.70", "6.71", "6.72",
    "7.00", "7.01", "7.02", "7.50", "7.51", "7.55",
    "8.00", "8.01", "8.03", "8.20", "8.50", "8.52",
    "9.00", "9.03", "9.04", "9.50", "9.51", "9.60",
    "10.00", "10.01", "10.50", "10.70", "10.71",
    "11.00", "11.02", "11.50",
}


@dataclass
class FirmwareInfo:
    """Information about a PS4 firmware file."""

    path: str
    filename: str
    size_bytes: int
    size_display: str
    version: str
    is_valid: bool
    sha256: str
    error: str = ""


class FirmwareManager:
    """Handles PS4 firmware import, validation, and management."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def validate_pup_file(self, filepath: str) -> FirmwareInfo:
        """Validate a .PUP firmware file and extract info."""
        path = Path(filepath)
        if not path.exists():
            return FirmwareInfo(
                path=filepath, filename="", size_bytes=0,
                size_display="0 B", version="", is_valid=False,
                sha256="", error="File not found",
            )

        filename = path.name
        size_bytes = path.stat().st_size
        size_display = self._format_size(size_bytes)

        if not filename.upper().endswith(".PUP"):
            return FirmwareInfo(
                path=filepath, filename=filename, size_bytes=size_bytes,
                size_display=size_display, version="", is_valid=False,
                sha256="", error="Not a .PUP file",
            )

        if size_bytes < 16:
            return FirmwareInfo(
                path=filepath, filename=filename, size_bytes=size_bytes,
                size_display=size_display, version="", is_valid=False,
                sha256="", error="File too small to be a valid firmware",
            )

        sha256 = self._compute_sha256(filepath)
        version = self._detect_version(filepath)
        is_valid = True

        try:
            with open(filepath, "rb") as f:
                magic = f.read(4)
                if magic != PUP_MAGIC:
                    return FirmwareInfo(
                        path=filepath, filename=filename, size_bytes=size_bytes,
                        size_display=size_display, version=version, is_valid=False,
                        sha256=sha256,
                        error="Invalid PUP magic bytes (not a valid PS4 firmware)",
                    )
        except OSError as e:
            return FirmwareInfo(
                path=filepath, filename=filename, size_bytes=size_bytes,
                size_display=size_display, version=version, is_valid=False,
                sha256=sha256, error=f"Read error: {e}",
            )

        return FirmwareInfo(
            path=filepath, filename=filename, size_bytes=size_bytes,
            size_display=size_display, version=version, is_valid=is_valid,
            sha256=sha256,
        )

    def import_firmware(self, filepath: str) -> FirmwareInfo:
        """Validate and import a firmware file into the launcher's firmware directory."""
        info = self.validate_pup_file(filepath)
        if not info.is_valid:
            return info

        dest = self._config.firmware_dir / info.filename
        try:
            shutil.copy2(filepath, dest)
        except OSError as e:
            info.is_valid = False
            info.error = f"Copy failed: {e}"
            return info

        self._config.set("firmware_path", str(dest))
        self._config.firmware_installed = True
        self._config.firmware_version = info.version or "Unknown"
        return info

    def uninstall_firmware(self) -> bool:
        """Remove installed firmware."""
        fw_path = self._config.get("firmware_path", "")
        if fw_path and Path(fw_path).exists():
            try:
                Path(fw_path).unlink()
            except OSError:
                pass
        self._config.set("firmware_path", "")
        self._config.firmware_installed = False
        self._config.firmware_version = ""
        return True

    def get_installed_firmware(self) -> FirmwareInfo | None:
        """Get info about currently installed firmware."""
        fw_path = self._config.get("firmware_path", "")
        if not fw_path or not Path(fw_path).exists():
            self._config.firmware_installed = False
            self._config.firmware_version = ""
            return None
        return self.validate_pup_file(fw_path)

    def _detect_version(self, filepath: str) -> str:
        """Attempt to detect firmware version from the PUP file header."""
        try:
            with open(filepath, "rb") as f:
                header = f.read(128)
                if len(header) >= 16:
                    version_field = struct.unpack_from("<I", header, 8)[0]
                    major = (version_field >> 24) & 0xFF
                    minor = (version_field >> 16) & 0xFF
                    version_str = f"{major}.{minor:02d}"
                    if version_str in KNOWN_VERSIONS:
                        return version_str
                    simplified = f"{major}.{minor}"
                    if simplified in KNOWN_VERSIONS:
                        return simplified
        except (OSError, struct.error):
            pass
        return ""

    @staticmethod
    def _compute_sha256(filepath: str) -> str:
        sha = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha.update(chunk)
        return sha.hexdigest()

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        for unit in ("B", "KB", "MB", "GB"):
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
