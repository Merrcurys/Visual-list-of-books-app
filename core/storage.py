"""Хранилище библиотеки на SQLite.

Основной формат — файл ``data/library.db``. Старый ``data/books-list.json``
при первом запуске автоматически переносится в базу, а сам файл остаётся
нетронутым (обратная совместимость). Импорт умеет читать и ``.db``, и ``.zip``
(в том числе архивы старого формата с ``books-list.json``).
"""

import json
import shutil
import sqlite3
import tempfile
import zipfile
from pathlib import Path

from . import images, paths

BASE_DIR = paths.app_dir()
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "library.db"
COVERS_DIR = DATA_DIR / "covers"
LEGACY_JSON = DATA_DIR / "books-list.json"
LEGACY_SETTINGS = DATA_DIR / "settings.json"

SORT_COLUMNS = {
    "id": "id",
    "name_book": "name_book",
    "name_autor": "name_autor",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_book TEXT NOT NULL,
    name_autor TEXT NOT NULL,
    cover TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
CREATE INDEX IF NOT EXISTS idx_quotes_book ON quotes(book_id, position);
"""

_connection = None
_covers_normalized = False


# --------------------------------------------------------------- соединение
def _connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def connection():
    """Ленивое подключение к базе с миграцией старого JSON."""
    global _connection
    if _connection is None:
        _connection = _connect()
        _connection.executescript(SCHEMA)
        _connection.commit()
        _migrate_legacy()
        normalize_covers()
    return _connection


def normalize_covers(force=False):
    """Конвертирует все обложки в WebP и обновляет пути в базе.

    Обеспечивает обратную совместимость: обложки из старых бэкапов
    (jpg/jpeg/png) переделываются в webp.
    """
    global _covers_normalized
    if _covers_normalized and not force:
        return 0
    _covers_normalized = True
    if not COVERS_DIR.exists():
        return 0

    conn = connection()
    converted = {}
    for file in list(COVERS_DIR.iterdir()):
        if not file.is_file() or file.name.startswith("."):
            continue
        suffix = file.suffix.lower()
        if suffix == images.WEBP_EXT or suffix not in images.SOURCE_EXTENSIONS:
            continue
        try:
            target = images.convert_to_webp(file)
        except Exception:
            continue
        try:
            file.unlink()
        except OSError:
            pass
        converted[file.stem] = target.name

    for row in conn.execute("SELECT id, cover FROM books").fetchall():
        cover = row["cover"] or ""
        if not cover or images.is_webp(cover):
            continue
        stem = Path(cover).stem
        target_name = converted.get(stem)
        if target_name is None:
            candidate = COVERS_DIR / f"{stem}{images.WEBP_EXT}"
            if candidate.exists():
                target_name = candidate.name
        if not target_name:
            continue
        separator = "\\" if "\\" in cover else "/"
        directory = (cover.rsplit(separator, 1)[0]
                     if separator in cover else "")
        new_cover = (f"{directory}{separator}{target_name}"
                     if directory else target_name)
        conn.execute("UPDATE books SET cover = ? WHERE id = ?",
                     (new_cover, row["id"]))
    conn.commit()
    return len(converted)


def _reconnect():
    global _connection
    if _connection is not None:
        _connection.close()
    _connection = _connect()
    _connection.executescript(SCHEMA)
    _connection.commit()


# --------------------------------------------------------- настройки (key/value)
def get_setting(key, default=None):
    row = connection().execute(
        "SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row is not None else default


def set_setting(key, value):
    conn = connection()
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, str(value)))
    conn.commit()


# ------------------------------------------------------------------ миграция
def _legacy_theme():
    try:
        with open(LEGACY_SETTINGS, "r", encoding="utf-8") as f:
            return json.load(f).get("theme")
    except (OSError, ValueError):
        return None


def _apply_legacy_sort(raw_sort):
    text = raw_sort.get("text", ["id", "id", 0])
    digits = raw_sort.get("digit", [0, 0, 0])
    set_setting("sort_key", text[0] if len(text) > 0 else "id")
    set_setting("sort_secondary", text[1] if len(text) > 1 else "id")
    set_setting("dir_id", digits[0] if len(digits) > 0 else 0)
    set_setting("dir_autor", digits[1] if len(digits) > 1 else 0)
    set_setting("dir_book", digits[2] if len(digits) > 2 else 0)


def _clear_library():
    conn = connection()
    conn.execute("DELETE FROM quotes")
    conn.execute("DELETE FROM books")
    conn.commit()


def _migrate_legacy(force_json=None):
    """Перенести старый JSON в базу (если база пуста и миграция не сделана)."""
    conn = connection()
    already = get_setting("json_migrated")
    empty = conn.execute("SELECT COUNT(*) AS n FROM books").fetchone()["n"] == 0
    if already and force_json is None:
        return False

    source = Path(force_json) if force_json else LEGACY_JSON
    if not source.exists():
        set_setting("json_migrated", 1)
        return False
    if force_json is None and not empty:
        set_setting("json_migrated", 1)
        return False

    try:
        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return False

    if force_json is not None:
        _clear_library()

    for book in data.get("books", []):
        conn.execute(
            "INSERT OR REPLACE INTO books (id, name_book, name_autor, cover) "
            "VALUES (?, ?, ?, ?)",
            (book.get("id"), book.get("name_book", ""),
             book.get("name_autor", ""), book.get("cover", "")))
        for position, quote in enumerate(book.get("quotes", [])):
            conn.execute(
                "INSERT INTO quotes (book_id, text, position) "
                "VALUES (?, ?, ?)", (book.get("id"), quote, position))
    conn.commit()

    _apply_legacy_sort(data.get("sort", {}))
    theme = _legacy_theme() if force_json is None else None
    if theme:
        set_setting("theme", theme)
    set_setting("json_migrated", 1)
    return True


# --------------------------------------------------------------------- книги
def _book_row_to_dict(row, quotes=None):
    return {
        "id": row["id"],
        "name_book": row["name_book"],
        "name_autor": row["name_autor"],
        "cover": row["cover"] or "",
        "quotes": quotes if quotes is not None else quotes_of(row["id"]),
    }


def quotes_of(book_id):
    rows = connection().execute(
        "SELECT text FROM quotes WHERE book_id = ? ORDER BY position, id",
        (book_id,)).fetchall()
    return [row["text"] for row in rows]


def get_books(sort_key="id", secondary="id", reverse=False):
    """Список книг с цитатами, отсортированный по ключам."""
    key = SORT_COLUMNS.get(sort_key, "id")
    second = SORT_COLUMNS.get(secondary, "id")
    direction = "DESC" if reverse else "ASC"
    rows = connection().execute(
        f"SELECT * FROM books ORDER BY {key} {direction}, "
        f"{second} {direction}").fetchall()
    return [_book_row_to_dict(row) for row in rows]


def get_book(book_id):
    row = connection().execute(
        "SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    return _book_row_to_dict(row) if row is not None else None


def count_books():
    return connection().execute(
        "SELECT COUNT(*) AS n FROM books").fetchone()["n"]


def next_book_id():
    return connection().execute(
        "SELECT COALESCE(MAX(id), 0) + 1 AS n FROM books").fetchone()["n"]


def add_book(name_book, name_autor, cover, book_id=None):
    conn = connection()
    cursor = conn.execute(
        "INSERT INTO books (id, name_book, name_autor, cover) "
        "VALUES (?, ?, ?, ?)",
        (book_id, name_book, name_autor, cover))
    conn.commit()
    return cursor.lastrowid if book_id is None else book_id


def update_book(book_id, name_book=None, name_autor=None, cover=None):
    fields, values = [], []
    if name_book is not None:
        fields.append("name_book = ?")
        values.append(name_book)
    if name_autor is not None:
        fields.append("name_autor = ?")
        values.append(name_autor)
    if cover is not None:
        fields.append("cover = ?")
        values.append(cover)
    if fields:
        values.append(book_id)
        connection().execute(
            f"UPDATE books SET {', '.join(fields)} WHERE id = ?", values)
        connection().commit()


def delete_book(book_id):
    connection().execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection().commit()


# -------------------------------------------------------------------- цитаты
def set_quotes(book_id, quotes):
    conn = connection()
    conn.execute("DELETE FROM quotes WHERE book_id = ?", (book_id,))
    conn.executemany(
        "INSERT INTO quotes (book_id, text, position) VALUES (?, ?, ?)",
        [(book_id, text, position) for position, text in enumerate(quotes)])
    conn.commit()


def add_quote(book_id, text):
    conn = connection()
    position = conn.execute(
        "SELECT COALESCE(MAX(position), -1) + 1 AS n FROM quotes "
        "WHERE book_id = ?", (book_id,)).fetchone()["n"]
    conn.execute(
        "INSERT INTO quotes (book_id, text, position) VALUES (?, ?, ?)",
        (book_id, text, position))
    conn.commit()


def remove_quote(book_id, text):
    conn = connection()
    conn.execute(
        "DELETE FROM quotes WHERE id = (SELECT id FROM quotes "
        "WHERE book_id = ? AND text = ? ORDER BY position, id LIMIT 1)",
        (book_id, text))
    conn.commit()


# ------------------------------------------------------------------- сортировка
def get_sort():
    """(ключ, вторичный ключ, обратный порядок) для текущей сортировки."""
    key = get_setting("sort_key", "id") or "id"
    secondary = get_setting("sort_secondary", "id") or "id"
    if key not in SORT_COLUMNS:
        key = "id"
    if secondary not in SORT_COLUMNS:
        secondary = "id"
    reverse = _direction(key) == 1
    return key, secondary, reverse


def _direction(key):
    mapping = {"id": "dir_id", "name_book": "dir_book",
               "name_autor": "dir_autor"}
    try:
        return int(get_setting(mapping[key], 0) or 0)
    except (TypeError, ValueError):
        return 0


def set_sort(key, secondary, reverse):
    set_setting("sort_key", key)
    set_setting("sort_secondary", secondary)
    set_direction(key, 1 if reverse else 0)


def set_direction(key, value):
    mapping = {"id": "dir_id", "name_book": "dir_book",
               "name_autor": "dir_autor"}
    set_setting(mapping[key], value)


def toggle_direction(key):
    value = 1 - _direction(key)
    set_direction(key, value)
    return value


# ------------------------------------------------------ экспорт / импорт
def export_database(destination):
    """Сохранить базу в отдельный файл .db."""
    connection()
    destination = Path(destination)
    source = sqlite3.connect(DB_PATH)
    target = sqlite3.connect(destination)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()
    return destination


def export_archive(destination):
    """Сохранить базу и обложки в zip-архив."""
    destination = Path(destination)
    with tempfile.TemporaryDirectory() as tmp:
        db_copy = Path(tmp) / "library.db"
        export_database(db_copy)
        with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(db_copy, arcname="library.db")
            if COVERS_DIR.exists():
                for file in sorted(COVERS_DIR.iterdir()):
                    if file.is_file() and not file.name.startswith("."):
                        zf.write(file, arcname=f"covers/{file.name}")
    return destination


def _copy_covers(source_dir):
    source = Path(source_dir)
    if not source.exists():
        return
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    for file in source.iterdir():
        if file.is_file() and not file.name.startswith("."):
            (COVERS_DIR / file.name).write_bytes(file.read_bytes())


def import_data(path):
    """Импортировать данные из .db или .zip. Возвращает строку-результат."""
    path = Path(path)
    if path.suffix.lower() == ".zip":
        result = _import_zip(path)
    else:
        _import_database(path)
        result = "database"
    normalize_covers(force=True)
    return result


def _import_database(db_file):
    source = sqlite3.connect(db_file)
    try:
        tables = {row[0] for row in source.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'")}
        if "books" not in tables:
            raise ValueError("Файл базы данных не содержит таблицу 'books'.")
    finally:
        source.close()
    if Path(db_file).resolve() == DB_PATH.resolve():
        return
    _replace_db(db_file)


def _import_zip(archive):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        with zipfile.ZipFile(archive, "r") as zf:
            zf.extractall(tmp_dir)
        _copy_covers(tmp_dir / "covers")
        db_file = tmp_dir / "library.db"
        legacy = tmp_dir / "books-list.json"
        if db_file.exists():
            _import_database(db_file)
            return "archive-db"
        if legacy.exists():
            _reconnect()
            _migrate_legacy(force_json=legacy)
            return "archive-json"
        raise ValueError(
            "Архив не содержит ни 'library.db', ни 'books-list.json'.")


def _replace_db(new_db_file):
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(new_db_file, DB_PATH)
    _reconnect()
    set_setting("json_migrated", 1)
