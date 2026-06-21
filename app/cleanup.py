from __future__ import annotations

import shutil
import time
from pathlib import Path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink(missing_ok=True)


def cleanup_old_tmp(tmp_dir: Path, max_age_hours: int = 12) -> None:
    if not tmp_dir.exists():
        return

    now = time.time()
    max_age_seconds = max_age_hours * 60 * 60
    for child in tmp_dir.iterdir():
        try:
            age = now - child.stat().st_mtime
            if age > max_age_seconds:
                remove_path(child)
        except OSError:
            continue
