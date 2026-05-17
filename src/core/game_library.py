"""PS4 game library management: scan, catalog, and organize games."""

import json
import os
import struct
from dataclasses import asdict, dataclass, field
from pathlib import Path

from src.core.config import Config


@dataclass
class GameEntry:
    """Represents a PS4 game in the library."""

    game_id: str
    title: str
    path: str
    title_id: str = ""
    region: str = ""
    size_display: str = ""
    cover_path: str = ""
    last_played: str = ""
    play_count: int = 0
    favorite: bool = False


class GameLibrary:
    """Manages the PS4 game library."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._library_file = config.config_dir / "library.json"
        self._games: list[GameEntry] = []
        self._load()

    def _load(self) -> None:
        if self._library_file.exists():
            try:
                with open(self._library_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._games = [GameEntry(**entry) for entry in data]
            except (json.JSONDecodeError, OSError, TypeError):
                self._games = []

    def _save(self) -> None:
        with open(self._library_file, "w", encoding="utf-8") as f:
            json.dump([asdict(g) for g in self._games], f, indent=2, ensure_ascii=False)

    @property
    def games(self) -> list[GameEntry]:
        return list(self._games)

    @property
    def count(self) -> int:
        return len(self._games)

    def add_game(self, path: str) -> GameEntry | None:
        """Add a game from a directory path."""
        game_dir = Path(path)
        if not game_dir.is_dir():
            return None

        for existing in self._games:
            if os.path.normpath(existing.path) == os.path.normpath(path):
                return existing

        info = self._extract_game_info(game_dir)
        game = GameEntry(
            game_id=info.get("title_id", game_dir.name),
            title=info.get("title", game_dir.name),
            path=str(game_dir),
            title_id=info.get("title_id", ""),
            region=info.get("region", ""),
            size_display=self._get_dir_size(game_dir),
        )

        cover = self._find_cover(game_dir)
        if cover:
            game.cover_path = str(cover)

        self._games.append(game)
        self._save()
        return game

    def remove_game(self, game_id: str) -> bool:
        """Remove a game from the library (does not delete files)."""
        for i, game in enumerate(self._games):
            if game.game_id == game_id:
                self._games.pop(i)
                self._save()
                return True
        return False

    def scan_directory(self, directory: str) -> list[GameEntry]:
        """Scan a directory for PS4 game folders and add them."""
        scan_dir = Path(directory)
        if not scan_dir.is_dir():
            return []

        added: list[GameEntry] = []
        for item in scan_dir.iterdir():
            if item.is_dir() and self._is_ps4_game(item):
                game = self.add_game(str(item))
                if game:
                    added.append(game)
        return added

    def get_game(self, game_id: str) -> GameEntry | None:
        for game in self._games:
            if game.game_id == game_id:
                return game
        return None

    def search(self, query: str) -> list[GameEntry]:
        query_lower = query.lower()
        return [g for g in self._games if query_lower in g.title.lower() or query_lower in g.title_id.lower()]

    def toggle_favorite(self, game_id: str) -> bool:
        game = self.get_game(game_id)
        if game:
            game.favorite = not game.favorite
            self._save()
            return True
        return False

    def update_last_played(self, game_id: str) -> None:
        from datetime import datetime
        game = self.get_game(game_id)
        if game:
            game.last_played = datetime.now().isoformat()
            game.play_count += 1
            self._save()
            recent = self._config.get("recent_games", [])
            if game_id in recent:
                recent.remove(game_id)
            recent.insert(0, game_id)
            self._config.set("recent_games", recent[:10])

    @staticmethod
    def _is_ps4_game(directory: Path) -> bool:
        """Check if a directory looks like a PS4 game dump."""
        markers = [
            directory / "eboot.bin",
            directory / "EBOOT.BIN",
            directory / "sce_sys" / "param.sfo",
            directory / "sce_sys" / "PARAM.SFO",
        ]
        return any(m.exists() for m in markers)

    @staticmethod
    def _extract_game_info(game_dir: Path) -> dict[str, str]:
        """Extract game info from param.sfo if available."""
        info: dict[str, str] = {}
        sfo_paths = [
            game_dir / "sce_sys" / "param.sfo",
            game_dir / "sce_sys" / "PARAM.SFO",
        ]

        sfo_path = None
        for p in sfo_paths:
            if p.exists():
                sfo_path = p
                break

        if not sfo_path:
            return info

        try:
            with open(sfo_path, "rb") as f:
                data = f.read()

            if len(data) < 20:
                return info

            magic = data[:4]
            if magic != b"\x00PSF":
                return info

            key_offset = struct.unpack_from("<I", data, 8)[0]
            data_offset = struct.unpack_from("<I", data, 12)[0]
            entry_count = struct.unpack_from("<I", data, 16)[0]

            for i in range(entry_count):
                entry_off = 20 + i * 16
                if entry_off + 16 > len(data):
                    break

                key_off = struct.unpack_from("<H", data, entry_off)[0]
                data_fmt = struct.unpack_from("<H", data, entry_off + 2)[0]
                data_len = struct.unpack_from("<I", data, entry_off + 4)[0]
                val_off = struct.unpack_from("<I", data, entry_off + 12)[0]

                key_start = key_offset + key_off
                key_end = data.index(b"\x00", key_start)
                key = data[key_start:key_end].decode("utf-8", errors="ignore")

                val_start = data_offset + val_off
                if data_fmt == 0x0204:
                    value = data[val_start:val_start + data_len].rstrip(b"\x00").decode("utf-8", errors="ignore")
                else:
                    continue

                if key == "TITLE":
                    info["title"] = value
                elif key == "TITLE_ID":
                    info["title_id"] = value
                elif key == "CONTENT_ID":
                    parts = value.split("-")
                    if len(parts) >= 1:
                        region_code = parts[0][:2] if parts[0] else ""
                        region_map = {"UP": "US", "EP": "EU", "JP": "JP", "HP": "HK", "KP": "KR"}
                        info["region"] = region_map.get(region_code, region_code)

        except (OSError, struct.error):
            pass

        return info

    @staticmethod
    def _find_cover(game_dir: Path) -> Path | None:
        cover_names = [
            "icon0.png", "ICON0.PNG", "icon0.jpg", "ICON0.JPG",
            "pic0.png", "PIC0.PNG", "pic1.png", "PIC1.PNG",
            "cover.png", "cover.jpg", "poster.png", "poster.jpg",
        ]
        sce_sys = game_dir / "sce_sys"
        search_dirs = [sce_sys, game_dir]
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for name in cover_names:
                candidate = search_dir / name
                if candidate.exists():
                    return candidate
        return None

    @staticmethod
    def _get_dir_size(directory: Path) -> str:
        total = 0
        try:
            for root, _dirs, files in os.walk(directory):
                for f in files:
                    fp = Path(root) / f
                    try:
                        total += fp.stat().st_size
                    except OSError:
                        pass
        except OSError:
            pass

        for unit in ("B", "KB", "MB", "GB"):
            if total < 1024:
                return f"{total:.1f} {unit}"
            total /= 1024
        return f"{total:.1f} TB"
