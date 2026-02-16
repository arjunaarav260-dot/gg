import os
import subprocess
import sys
from pathlib import Path

print('Dev : @FFJFF5 | Channel : @EgyCodes')

BASE_DIR = Path(__file__).resolve().parent
VENDOR_DIR = BASE_DIR / 'vendor' / 'telegram'

REPOSITORIES = {
    'PyrogramMod': 'https://github.com/PyrogramMod/PyrogramMod',
    'Telethon': 'https://github.com/LonamiWebs/Telethon',
    'pyTelegramBotAPI': 'https://github.com/eternnoir/pyTelegramBotAPI',
}


def ensure_repo(name: str, url: str) -> None:
    repo_path = VENDOR_DIR / name
    VENDOR_DIR.mkdir(parents=True, exist_ok=True)
    if repo_path.exists():
        print(f'[OK] {name} already present at {repo_path}')
        return

    print(f'[CLONE] {name} <- {url}')
    subprocess.run(['git', 'clone', '--depth', '1', url, str(repo_path)], check=True)


def ensure_pip(module_name: str, package_name: str | None = None) -> None:
    package_name = package_name or module_name
    try:
        __import__(module_name)
        print(f'[OK] python module: {module_name}')
    except Exception:
        print(f'[PIP] installing: {package_name}')
        subprocess.run([sys.executable, '-m', 'pip', 'install', package_name], check=True)


for repo_name, repo_url in REPOSITORIES.items():
    ensure_repo(repo_name, repo_url)

# Keep only non-Telegram dependencies here.
ensure_pip('kvsqlite')
ensure_pip('schedule')
ensure_pip('user_agent')
ensure_pip('aiosqlite')
ensure_pip('opentele')
