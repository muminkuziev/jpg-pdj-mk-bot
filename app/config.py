import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    tmp_dir: Path
    max_images: int
    max_file_mb: int
    render_external_url: str
    port: int

    @property
    def max_file_bytes(self) -> int:
        return self.max_file_mb * 1024 * 1024


def get_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    return Settings(
        bot_token=token,
        tmp_dir=Path(os.getenv("TMP_DIR", "tmp")),
        max_images=int(os.getenv("MAX_IMAGES", "20")),
        max_file_mb=int(os.getenv("MAX_FILE_MB", "10")),
        render_external_url=os.getenv("RENDER_EXTERNAL_URL", "").strip().rstrip("/"),
        port=int(os.getenv("PORT", "10000")),
    )
