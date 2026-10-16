"""Оформление приложения: светлая и тёмная темы.

Модуль хранит цветовые токены тем, собирает QSS-таблицу стилей и следит за
выбранной темой, сохраняя её в базе данных (``core.storage``).
"""

from PyQt6 import QtCore, QtGui

THEMES = {
    "light": {
        "window_bg": "#F4F6FA",
        "surface": "#FFFFFF",
        "surface_alt": "#F1F3FA",
        "border": "#E2E6F0",
        "text": "#1B1F2A",
        "text_secondary": "#6A7280",
        "text_disabled": "#A8AEBB",
        "accent": "#F97316",
        "accent_hover": "#EA6A0B",
        "accent_pressed": "#D95E06",
        "accent_text": "#FFFFFF",
        "accent_soft": "#FDECE0",
        "hover": "#F0F2FA",
        "pressed": "#E5E8F4",
        "scroll": "#CDD3E2",
        "danger": "#E5484D",
    },
    "dark": {
        "window_bg": "#1B1B1B",
        "surface": "#212121",
        "surface_alt": "#272727",
        "border": "#343434",
        "text": "#EDEDED",
        "text_secondary": "#A3A3A3",
        "text_disabled": "#606060",
        "accent": "#FB923C",
        "accent_hover": "#FFA65C",
        "accent_pressed": "#E97F26",
        "accent_text": "#201207",
        "accent_soft": "#3D2A18",
        "hover": "#2C2C2C",
        "pressed": "#343434",
        "scroll": "#3E3E3E",
        "danger": "#FF6B6B",
    },
}

_QSS = """
* {
    font-family: "Segoe UI", "Inter", "Roboto", "Helvetica Neue", sans-serif;
    font-size: 13px;
    outline: none;
}

QWidget {
    color: %(text)s;
}

QMainWindow, QDialog {
    background: %(window_bg)s;
}

QLabel {
    background: transparent;
    color: %(text)s;
}

QToolTip {
    background: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: 8px;
    padding: 6px 10px;
}

QLabel#PageNumber {
    color: %(text_secondary)s;
    font-size: 13px;
    font-weight: 600;
}

QLabel#SettingsName {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: 3px;
    color: %(text)s;
}

QLabel#SettingsSubtitle {
    color: %(text_secondary)s;
    font-size: 13px;
}

QLabel#BookName, QLabel#AutorName {
    font-size: 15px;
    font-weight: 600;
    color: %(text_secondary)s;
}

QLabel#ErrorText {
    font-size: 14px;
    font-weight: 600;
    color: %(danger)s;
}

QLabel#label {
    font-size: 11px;
    color: %(text_disabled)s;
}

QPushButton {
    background: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: 12px;
    padding: 6px 12px;
    font-weight: 600;
}

QPushButton:hover {
    background: %(hover)s;
    border-color: %(accent)s;
}

QPushButton:pressed {
    background: %(pressed)s;
}

QPushButton:disabled {
    color: %(text_disabled)s;
    border-color: %(border)s;
}

QPushButton#AddBookButton {
    background: %(accent)s;
    color: %(accent_text)s;
    border: none;
    border-radius: 12px;
    padding: 8px 14px;
    font-weight: 700;
}

QPushButton#AddBookButton:hover {
    background: %(accent_hover)s;
}

QPushButton#AddBookButton:pressed {
    background: %(accent_pressed)s;
}

QPushButton#SwipeLeftButton, QPushButton#SwipeRightButton {
    border-radius: 10px;
    padding: 0;
    font-size: 15px;
    font-weight: 700;
    color: %(text_secondary)s;
}

QPushButton#SwipeLeftButton:hover, QPushButton#SwipeRightButton:hover {
    color: %(accent)s;
    border-color: %(accent)s;
    background: %(accent_soft)s;
}

QPushButton#Settings, QPushButton#ThemeButton, QPushButton#SortButton {
    background: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: 12px;
    padding: 0;
    color: %(text_secondary)s;
}

QPushButton#Settings:hover, QPushButton#ThemeButton:hover,
QPushButton#SortButton:hover {
    background: %(accent_soft)s;
    border-color: %(accent)s;
}

QPushButton#ReadyButtonAddBook, QPushButton#ReadyButtonAddText,
QPushButton#AddQuoteButton {
    background: %(accent)s;
    color: %(accent_text)s;
    border: none;
    border-radius: 12px;
    padding: 7px 12px;
    font-weight: 700;
}

QPushButton#ReadyButtonAddBook:hover, QPushButton#ReadyButtonAddText:hover,
QPushButton#AddQuoteButton:hover {
    background: %(accent_hover)s;
}

QPushButton#ReadyButtonAddBook:pressed, QPushButton#ReadyButtonAddText:pressed,
QPushButton#AddQuoteButton:pressed {
    background: %(accent_pressed)s;
}

QFrame#settingsCard {
    background: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: 20px;
}

QFrame#settingsCard:hover {
    background: %(accent_soft)s;
    border: 1px solid %(accent)s;
}

QLabel#cardTitle {
    font-size: 19px;
    font-weight: 700;
    color: %(text)s;
}

QLabel#cardText {
    color: %(text_secondary)s;
    font-size: 12px;
}

QMenu {
    background: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: 12px;
    padding: 6px;
}

QMenu::item {
    padding: 8px 16px 8px 32px;
    border-radius: 8px;
    color: %(text)s;
}

QMenu::item:selected {
    background: %(accent_soft)s;
    color: %(accent)s;
}

QMenu::separator {
    height: 1px;
    background: %(border)s;
    margin: 6px 10px;
}

QLineEdit {
    background: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: 10px;
    padding: 8px 12px;
    color: %(text)s;
    selection-background-color: %(accent)s;
    selection-color: %(accent_text)s;
}

QLineEdit:hover {
    border-color: %(accent)s;
}

QLineEdit:focus {
    border: 1px solid %(accent)s;
    background: %(surface)s;
}

QFrame#quoteCard {
    background: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: 14px;
}

QFrame#quoteCard:hover {
    border-color: %(accent)s;
}

QFrame#quoteCard[selected="true"] {
    background: %(accent_soft)s;
    border: 1px solid %(accent)s;
}

QFrame#quoteCard QLabel#quoteText {
    color: %(text)s;
    font-size: 15px;
    background: transparent;
}

QPushButton#coverOverlay {
    background: transparent;
    border: none;
    border-radius: 8px;
}

QPushButton#AddCoverButton {
    background: %(surface_alt)s;
    border: 2px dashed %(border)s;
    border-radius: 14px;
    color: %(text_secondary)s;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#AddCoverButton:hover {
    background: %(accent_soft)s;
    border-color: %(accent)s;
    color: %(accent)s;
}

QPushButton#AddCoverButton[hasCover="true"] {
    background: transparent;
    border: none;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QWidget#quotesContainer {
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px 0;
}

QScrollBar::handle:vertical {
    background: %(scroll)s;
    border-radius: 5px;
    min-height: 28px;
}

QScrollBar::handle:vertical:hover {
    background: %(accent)s;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}

QInputDialog, QMessageBox {
    background: %(window_bg)s;
}

QInputDialog QPushButton, QMessageBox QPushButton {
    min-width: 88px;
}
"""

_current_theme = None


def get_stylesheet(theme=None):
    """Собрать QSS для темы (по умолчанию — активной)."""
    tokens = THEMES[theme or get_theme()]
    return _QSS % tokens


def get_theme():
    """Активная тема с ленивой загрузкой из настроек."""
    global _current_theme
    if _current_theme is None:
        _current_theme = _load_theme()
    return _current_theme


def set_theme(name):
    """Сделать тему активной и сохранить выбор."""
    global _current_theme
    _current_theme = name if name in THEMES else "light"
    _save_theme(_current_theme)
    return _current_theme


def toggle_theme():
    """Переключить светлую и тёмную темы."""
    return set_theme("dark" if get_theme() == "light" else "light")


def apply_theme(app, theme=None):
    """Применить тему ко всему приложению."""
    app.setStyleSheet(get_stylesheet(theme))


def _system_theme():
    """Тема оформления, выбранная в системе."""
    hints = QtGui.QGuiApplication.styleHints()
    scheme = getattr(hints, "colorScheme", None)
    if scheme is not None:
        value = scheme()
        if value == QtCore.Qt.ColorScheme.Dark:
            return "dark"
        if value == QtCore.Qt.ColorScheme.Light:
            return "light"
    return "light"


def _load_theme():
    try:
        from core import storage
        stored = storage.get_setting("theme")
    except Exception:
        stored = None
    if stored in THEMES:
        return stored
    return _system_theme()


def _save_theme(name):
    try:
        from core import storage
        storage.set_setting("theme", name)
    except Exception:
        pass


def theme_color(key="text_secondary"):
    """QColor одного из токенов активной темы."""
    return QtGui.QColor(THEMES[get_theme()][key])


# Цвета фона (верх, низ) для плавного градиента без полос.
BACKGROUND_STOPS = {
    "light": ((249, 250, 253), (232, 235, 244)),
    "dark": ((22, 22, 22), (35, 35, 35)),
}

_BACKGROUND_CACHE = {}


def background_pixmap(size):
    """Плавный вертикальный градиент фона с дизерингом (без полос).

    QSS-градиент квантуется до 8-бит и даёт видимые ступени, поэтому фон
    рисуется по строкам с распределением ошибки округления — переходы
    становятся мягкими.
    """
    key = (get_theme(), size.width(), size.height())
    cached = _BACKGROUND_CACHE.get(key)
    if cached is not None:
        return cached

    width = max(1, size.width())
    height = max(1, size.height())
    top, bottom = BACKGROUND_STOPS.get(get_theme(), BACKGROUND_STOPS["light"])

    image = QtGui.QImage(width, height, QtGui.QImage.Format.Format_RGB888)
    painter = QtGui.QPainter(image)
    errors = [0.0, 0.0, 0.0]
    for y in range(height):
        ratio = y / (height - 1) if height > 1 else 0.0
        color = []
        for index in range(3):
            target = (top[index]
                      + (bottom[index] - top[index]) * ratio + errors[index])
            value = int(round(target))
            value = 0 if value < 0 else 255 if value > 255 else value
            errors[index] = target - value
            color.append(value)
        painter.setPen(QtGui.QColor(*color))
        painter.drawLine(0, y, width, y)
    painter.end()

    pixmap = QtGui.QPixmap.fromImage(image)
    _BACKGROUND_CACHE[key] = pixmap
    return pixmap


def cover_shadow():
    """Параметры мягкой тени под обложками (зависят от темы)."""
    if get_theme() == "dark":
        return {"blurRadius": 34, "xOffset": 0, "yOffset": 14,
                "color": QtGui.QColor(0, 0, 0, 170)}
    return {"blurRadius": 30, "xOffset": 0, "yOffset": 14,
            "color": QtGui.QColor(28, 28, 28, 74)}


def card_shadow():
    """Параметры тени для карточек с цитатами."""
    if get_theme() == "dark":
        return {"blurRadius": 28, "xOffset": 0, "yOffset": 10,
                "color": QtGui.QColor(0, 0, 0, 120)}
    return {"blurRadius": 24, "xOffset": 0, "yOffset": 10,
            "color": QtGui.QColor(28, 28, 28, 48)}


def rounded_pixmap(pixmap, target_size, radius=14):
    """Скруглённая копия обложки нужного размера."""
    if pixmap is None or pixmap.isNull() or not target_size:
        return pixmap
    width, height = target_size
    scaled = pixmap.scaled(
        QtCore.QSize(width, height),
        QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation)
    rounded = QtGui.QPixmap(width, height)
    rounded.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(rounded)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(
        QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
    path = QtGui.QPainterPath()
    path.addRoundedRect(
        QtCore.QRectF(0, 0, width, height), radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, scaled)
    painter.end()
    return rounded
