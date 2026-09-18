"""خواننده ساده فایل .env بدون نیاز به پکیج اضافه."""
import os
from pathlib import Path

_LOADED = False


def load_env(path: Path) -> None:
    """مقادیر فایل .env را در متغیرهای محیطی بارگذاری می‌کند."""
    global _LOADED
    if _LOADED or not path.exists():
        _LOADED = True
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)
    _LOADED = True


def get(key: str, default=None):
    return os.environ.get(key, default)


def get_bool(key: str, default: bool = False) -> bool:
    value = os.environ.get(key)
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_int(key: str, default: int = 0) -> int:
    try:
        return int(os.environ.get(key, default))
    except (TypeError, ValueError):
        return default


def get_list(key: str, default=None):
    value = os.environ.get(key)
    if not value:
        return list(default or [])
    return [item.strip() for item in value.split(",") if item.strip()]
