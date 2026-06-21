from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from pathlib import Path

from .cleanup import ensure_dir, remove_path


@dataclass
class UserSession:
    mode: str
    folder: Path
    images: list[Path] = field(default_factory=list)


class SessionStore:
    def __init__(self, tmp_dir: Path) -> None:
        self.tmp_dir = tmp_dir
        self._sessions: dict[int, UserSession] = {}
        ensure_dir(tmp_dir)

    def start(self, user_id: int, mode: str) -> UserSession:
        self.cancel(user_id)
        folder = self.tmp_dir / str(user_id) / uuid.uuid4().hex[:12]
        ensure_dir(folder)
        session = UserSession(mode=mode, folder=folder)
        self._sessions[user_id] = session
        return session

    def get(self, user_id: int) -> UserSession | None:
        return self._sessions.get(user_id)

    def add_image(self, user_id: int, path: Path) -> int:
        session = self._sessions[user_id]
        session.images.append(path)
        return len(session.images)

    def cancel(self, user_id: int) -> None:
        session = self._sessions.pop(user_id, None)
        if session:
            remove_path(session.folder)
