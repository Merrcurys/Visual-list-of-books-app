"""Обложки хранятся в формате WebP, чтобы занимать меньше места."""

from pathlib import Path

from PIL import Image

WEBP_EXT = ".webp"
WEBP_QUALITY = 90
SOURCE_EXTENSIONS = {
    ".jpg", ".jpeg", ".jfif", ".png", ".bmp", ".gif", ".tif", ".tiff",
}


def _normalized(image):
    """Приводит изображение к RGB/RGBA — поддерживаемым в WebP режимам."""
    if "A" in image.getbands() or "transparency" in image.info:
        return image.convert("RGBA")
    return image.convert("RGB")


def save_as_webp(image, destination, quality=WEBP_QUALITY):
    """Сохраняет PIL-изображение в WebP, возвращает путь с расширением .webp."""
    destination = Path(destination)
    if destination.suffix.lower() != WEBP_EXT:
        destination = destination.with_suffix(WEBP_EXT)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _normalized(image).save(destination, format="WEBP", quality=quality)
    return destination


def convert_to_webp(source, destination=None, quality=WEBP_QUALITY):
    """Конвертирует файл изображения в WebP, возвращает путь к результату."""
    source = Path(source)
    if destination is None:
        destination = source.with_suffix(WEBP_EXT)
    destination = Path(destination)
    if source.resolve() == destination.resolve():
        return destination
    with Image.open(source) as image:
        save_as_webp(image, destination, quality)
    return destination


def is_webp(path):
    return Path(path).suffix.lower() == WEBP_EXT
