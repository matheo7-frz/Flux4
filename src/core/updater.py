"""Systeme de mise a jour automatique pour Flux4."""

import json
import urllib.request
from dataclasses import dataclass

APP_VERSION = "1.0.0"
GITHUB_REPO = "matheo7-frz/Flux4"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_RELEASES_URL = f"https://github.com/{GITHUB_REPO}/releases"


@dataclass
class UpdateInfo:
    """Informations sur une mise a jour disponible."""

    available: bool
    current_version: str
    latest_version: str
    release_url: str
    release_notes: str
    error: str = ""


def check_for_updates() -> UpdateInfo:
    """Verifier si une nouvelle version est disponible sur GitHub."""
    try:
        req = urllib.request.Request(
            GITHUB_API_URL,
            headers={"User-Agent": "Flux4/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        tag = data.get("tag_name", "")
        latest = tag.lstrip("vV")
        notes = data.get("body", "")
        html_url = data.get("html_url", GITHUB_RELEASES_URL)

        if not latest:
            return UpdateInfo(
                available=False,
                current_version=APP_VERSION,
                latest_version=APP_VERSION,
                release_url=GITHUB_RELEASES_URL,
                release_notes="",
            )

        is_newer = _compare_versions(latest, APP_VERSION)

        return UpdateInfo(
            available=is_newer,
            current_version=APP_VERSION,
            latest_version=latest,
            release_url=html_url,
            release_notes=notes[:500],
        )

    except Exception as e:
        return UpdateInfo(
            available=False,
            current_version=APP_VERSION,
            latest_version=APP_VERSION,
            release_url=GITHUB_RELEASES_URL,
            release_notes="",
            error=str(e),
        )


def _compare_versions(latest: str, current: str) -> bool:
    """Comparer deux versions semver. Retourne True si latest > current."""
    try:
        latest_parts = [int(x) for x in latest.split(".")]
        current_parts = [int(x) for x in current.split(".")]
        while len(latest_parts) < 3:
            latest_parts.append(0)
        while len(current_parts) < 3:
            current_parts.append(0)
        return latest_parts > current_parts
    except (ValueError, IndexError):
        return False
