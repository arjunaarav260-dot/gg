"""Load Telegram libraries from official upstream source repositories."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VENDOR_DIR = BASE_DIR / "vendor" / "telegram"

REPOSITORIES = {
    "PyrogramMod": "https://github.com/PyrogramMod/PyrogramMod",
    "Telethon": "https://github.com/LonamiWebs/Telethon",
    "pyTelegramBotAPI": "https://github.com/eternnoir/pyTelegramBotAPI",
}


class OfficialSourceError(RuntimeError):
    """Raised when official Telegram sources cannot be prepared."""


def _run_git(*args: str) -> None:
    subprocess.run(["git", *args], check=True)


def _ensure_repo(name: str, url: str) -> Path:
    repo_path = VENDOR_DIR / name
    VENDOR_DIR.mkdir(parents=True, exist_ok=True)

    if not repo_path.exists():
        try:
            _run_git("clone", "--depth", "1", url, str(repo_path))
        except subprocess.CalledProcessError as exc:
            raise OfficialSourceError(
                f"Failed to clone required official repository {url} to {repo_path}."
            ) from exc

    return repo_path


def _prepend_path(path: Path) -> None:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


def ensure_official_sources() -> None:
    paths = {name: _ensure_repo(name, url) for name, url in REPOSITORIES.items()}
    _prepend_path(paths["PyrogramMod"])
    _prepend_path(paths["Telethon"])
    _prepend_path(paths["pyTelegramBotAPI"])
