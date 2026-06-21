from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

A4_SIZE = (1240, 1754)
A4_MARGIN = 70


def load_image(path: Path) -> Image.Image:
    image = Image.open(path)
    image = ImageOps.exif_transpose(image)
    return image.convert("RGB")


def fit_to_a4(image: Image.Image) -> Image.Image:
    page_width, page_height = A4_SIZE
    max_width = page_width - A4_MARGIN * 2
    max_height = page_height - A4_MARGIN * 2

    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    page = Image.new("RGB", A4_SIZE, "white")
    x = (page_width - image.width) // 2
    y = (page_height - image.height) // 2
    page.paste(image, (x, y))
    return page


def enhance_for_document(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=2)
    gray = ImageEnhance.Contrast(gray).enhance(1.65)
    gray = ImageEnhance.Sharpness(gray).enhance(1.45)
    return gray.convert("RGB")


def prepare_image(path: Path, scan_mode: bool) -> Image.Image:
    image = load_image(path)
    if scan_mode:
        image = enhance_for_document(image)
    return fit_to_a4(image)
