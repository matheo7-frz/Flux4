"""shadPS4 emulator detection, download, and launch management."""

import os
import platform
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

from src.core.config import Config

SHADPS4_RELEASES_URL = "https://github.com/shadps4-emu/shadPS4/releases"
SHADPS4_API_URL = "https://api.github.com/repos/shadps4-emu/shadPS4/releases/latest"

EMULATOR_BINARY_NAMES = {
    "Windows": ["shadps4.exe", "Shadps4.exe", "shadPS4.exe"],
    "Linux": ["shadps4", "Shadps4", "shadPS4"],
    "Darwin": ["shadps4", "Shadps4", "shadPS4"],
}


class EmulatorManager:
    """Manages shadPS4 emulator detection and game launching."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def detect_emulator(self) -> str | None:
        """Try to find shadPS4 on the system. Returns path if found."""
        configured_path = self._config.emulator_path
        if configured_path and Path(configured_path).exists():
            return configured_path

        system = platform.system()
        binary_names = EMULATOR_BINARY_NAMES.get(system, ["shadps4"])

        for name in binary_names:
            found = shutil.which(name)
            if found:
                self._config.emulator_path = found
                return found

        common_paths = self._get_common_paths(system)
        for search_dir in common_paths:
            if not search_dir.exists():
                continue
            for name in binary_names:
                candidate = search_dir / name
                if candidate.exists() and os.access(candidate, os.X_OK):
                    self._config.emulator_path = str(candidate)
                    return str(candidate)

        return None

    def is_installed(self) -> bool:
        return self.detect_emulator() is not None

    def set_emulator_path(self, path: str) -> bool:
        """Manually set the emulator path."""
        if Path(path).exists():
            self._config.emulator_path = path
            return True
        return False

    def launch_game(self, game_path: str) -> subprocess.Popen | None:
        """Launch a game using shadPS4."""
        emu_path = self.detect_emulator()
        if not emu_path:
            return None

        eboot = self._find_eboot(game_path)
        if not eboot:
            return None

        cmd = [emu_path, str(eboot)]

        fw_path = self._config.get("firmware_path", "")
        if fw_path and Path(fw_path).exists():
            cmd.extend(["--firmware", fw_path])

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(Path(emu_path).parent),
            )
            return process
        except OSError:
            return None

    def get_download_url(self) -> str:
        """Get the latest shadPS4 release page URL."""
        return SHADPS4_RELEASES_URL

    def download_latest(self, dest_dir: str, progress_callback=None) -> str | None:
        """Download the latest shadPS4 release. Returns path to extracted binary."""
        try:
            req = urllib.request.Request(
                SHADPS4_API_URL,
                headers={"User-Agent": "PS4-Emu-Launcher/1.0"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                import json
                release_data = json.loads(resp.read().decode())
        except Exception:
            return None

        system = platform.system().lower()
        arch = platform.machine().lower()
        target_keywords = []

        if system == "windows":
            target_keywords = ["win", "windows"]
        elif system == "linux":
            target_keywords = ["linux"]
        elif system == "darwin":
            target_keywords = ["mac", "macos", "darwin"]

        download_url = None
        for asset in release_data.get("assets", []):
            name = asset["name"].lower()
            if any(kw in name for kw in target_keywords) and name.endswith(".zip"):
                download_url = asset["browser_download_url"]
                break

        if not download_url:
            for asset in release_data.get("assets", []):
                name = asset["name"].lower()
                if any(kw in name for kw in target_keywords):
                    download_url = asset["browser_download_url"]
                    break

        if not download_url:
            return None

        dest_path = Path(dest_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        zip_path = dest_path / "shadps4_latest.zip"

        try:
            req = urllib.request.Request(
                download_url,
                headers={"User-Agent": "PS4-Emu-Launcher/1.0"},
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                with open(zip_path, "wb") as f:
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total > 0:
                            progress_callback(downloaded / total)
        except Exception:
            if zip_path.exists():
                zip_path.unlink()
            return None

        try:
            extract_dir = dest_path / "shadps4"
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)
            zip_path.unlink()

            binary_names = EMULATOR_BINARY_NAMES.get(platform.system(), ["shadps4"])
            for root, _dirs, files in os.walk(extract_dir):
                for name in binary_names:
                    if name in files:
                        binary_path = Path(root) / name
                        if system == "linux" or system == "darwin":
                            binary_path.chmod(0o755)
                        self._config.emulator_path = str(binary_path)
                        return str(binary_path)
        except Exception:
            pass

        return None

    @staticmethod
    def _find_eboot(game_path: str) -> Path | None:
        """Find the EBOOT.BIN file in a game directory."""
        game_dir = Path(game_path)
        if game_dir.is_file() and game_dir.name.upper() == "EBOOT.BIN":
            return game_dir

        eboot = game_dir / "eboot.bin"
        if eboot.exists():
            return eboot

        for variant in ("EBOOT.BIN", "eboot.bin", "Eboot.bin"):
            candidate = game_dir / variant
            if candidate.exists():
                return candidate

        for root, _dirs, files in os.walk(game_dir):
            for f in files:
                if f.upper() == "EBOOT.BIN":
                    return Path(root) / f

        return None

    @staticmethod
    def _get_common_paths(system: str) -> list[Path]:
        home = Path.home()
        if system == "Windows":
            return [
                home / "Desktop" / "shadPS4",
                home / "Downloads" / "shadPS4",
                Path("C:/Program Files/shadPS4"),
                Path("C:/Program Files (x86)/shadPS4"),
                Path("C:/shadPS4"),
            ]
        elif system == "Linux":
            return [
                home / "shadPS4",
                home / ".local" / "bin",
                home / "Applications" / "shadPS4",
                Path("/usr/local/bin"),
                Path("/opt/shadPS4"),
                home / "Downloads" / "shadPS4",
            ]
        elif system == "Darwin":
            return [
                home / "Applications" / "shadPS4",
                Path("/Applications/shadPS4"),
                home / "Downloads" / "shadPS4",
            ]
        return []
