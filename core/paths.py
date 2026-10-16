"""Пути приложения с учётом работы из собранного exe (PyInstaller).

Изменяемые данные (база, обложки) хранятся рядом с exe, а статические
ресурсы (шрифт, иконки) берутся из бандла, если он есть.
"""

import sys
from pathlib import Path


def is_frozen():
    return getattr(sys, "frozen", False)


def app_dir():
    """Папка изменяемых данных: рядом с exe или корень проекта при разработке."""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def bundle_dir():
    """Папка статических ресурсов (у собранного exe — распакованный бандл)."""
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", app_dir()))
    return app_dir()


def data_dir():
    return app_dir() / "data"


def covers_dir():
    return data_dir() / "covers"


def resource(*parts):
    """Путь к статическому ресурсу: сначала бандл, затем папка рядом с exe."""
    relative = Path(*parts)
    for base in (bundle_dir(), app_dir()):
        candidate = base / relative
        if candidate.exists():
            return candidate
    return bundle_dir() / relative


def resolve(path):
    """Абсолютный путь для значений вида './data/covers/cover1.webp'."""
    if path is None:
        return None
    result = Path(path)
    return result if result.is_absolute() else app_dir() / result
