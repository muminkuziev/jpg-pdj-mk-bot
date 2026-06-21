from __future__ import annotations

from pathlib import Path

from .image_processing import prepare_image


def build_pdf(image_paths: list[Path], output_path: Path, scan_mode: bool) -> Path:
    if not image_paths:
        raise ValueError("At least one image is required")

    pages = [prepare_image(path, scan_mode=scan_mode) for path in image_paths]
    first, rest = pages[0], pages[1:]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    first.save(output_path, "PDF", resolution=150.0, save_all=True, append_images=rest)
    return output_path
