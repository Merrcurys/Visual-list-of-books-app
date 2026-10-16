from core import images, paths, storage
from template.add_book_interface import Ui_Form
from template.design import cover_shadow, rounded_pixmap

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QFileDialog, QGraphicsDropShadowEffect, QMessageBox)
from PIL import Image, ImageColor, ImageDraw, ImageFont

FONT_PATH = paths.resource("data", "font", "Roboto-Black.ttf")
COVER_SIZE = (360, 540)

COVER_THEMES = [
    ("#3B4A8C", "#1B2140"),
    ("#2E6E8E", "#122E3B"),
    ("#7A4A8C", "#2A1633"),
    ("#8C5A3B", "#3A2114"),
    ("#2F7A5E", "#123024"),
    ("#8C3B57", "#3A1522"),
]


def _gradient(size, top, bottom):
    """Вертикальный градиент из двух цветов."""
    width, height = size
    top_rgb = ImageColor.getrgb(top)
    bottom_rgb = ImageColor.getrgb(bottom)
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        ratio = y / (height - 1)
        color = tuple(round(a + (b - a) * ratio)
                      for a, b in zip(top_rgb, bottom_rgb))
        draw.line([(0, y), (width, y)], fill=color)
    return image


def _wrap_text(draw, text, font, max_width):
    """Разбивает текст на строки по ширине."""
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _load_font(size):
    """Шрифт обложки; если файла нет — встроенный запасной шрифт."""
    try:
        return ImageFont.truetype(str(FONT_PATH), size=size)
    except OSError:
        return ImageFont.load_default(size=size)


def _fit_title(draw, text, max_width, max_lines):
    """Подбирает размер шрифта, чтобы заголовок влезал в max_lines строк."""
    size = 46
    font = _load_font(size)
    lines = _wrap_text(draw, text, font, max_width)
    while len(lines) > max_lines and size > 22:
        size -= 2
        font = _load_font(size)
        lines = _wrap_text(draw, text, font, max_width)
    return font, lines


def cover_image(name_book, name_autor):
    """Рисует обложку в современном стиле и возвращает PIL-изображение."""
    width, height = COVER_SIZE
    top, bottom = COVER_THEMES[
        sum(ord(ch) for ch in name_book) % len(COVER_THEMES)]
    image = _gradient((width, height), top, bottom)
    draw = ImageDraw.Draw(image, "RGBA")

    # Корешок книги
    draw.rectangle([0, 0, 18, height], fill=(0, 0, 0, 70))
    draw.line([(18, 0), (18, height)], fill=(255, 255, 255, 26), width=2)

    # Внутренняя рамка
    draw.rounded_rectangle(
        [30, 30, width - 30, height - 30], radius=20,
        outline=(255, 255, 255, 40), width=2)

    # Название книги с мягкой тенью под текстом
    title_font, title_lines = _fit_title(draw, name_book, width - 130, 4)
    line_height = title_font.size + 8
    y = int(height * 0.42 - line_height * len(title_lines) / 2)
    for line in title_lines:
        line_width = draw.textlength(line, font=title_font)
        draw.text(((width - line_width) / 2 + 1, y + 2), line,
                  font=title_font, fill=(0, 0, 0, 90))
        draw.text(((width - line_width) / 2, y), line,
                  font=title_font, fill=(250, 250, 252))
        y += line_height

    # Разделитель
    divider_y = y + 18
    draw.line([(width * 0.32, divider_y), (width * 0.68, divider_y)],
              fill=(255, 255, 255, 120), width=2)

    # Автор
    autor_font = _load_font(22)
    autor_lines = _wrap_text(
        draw, name_autor, autor_font, width - 130)[:2]
    y = divider_y + 16
    for line in autor_lines:
        line_width = draw.textlength(line, font=autor_font)
        draw.text((width / 2 - line_width / 2, y), line,
                  font=autor_font, fill=(255, 255, 255, 190))
        y += autor_font.size + 6

    return image


def render_cover(name_book, name_autor, path):
    """Рисует обложку и сохраняет её в WebP по указанному пути."""
    return str(images.save_as_webp(cover_image(name_book, name_autor), path))


class AddBookPage(QWidget, Ui_Form):
    """Страница добавления и редактирования книги."""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.book_id = None
        self.cover_image = ""
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.ReadyButtonAddBook.clicked.connect(self.ready_add_book)
        self.AddCoverButton.clicked.connect(self.get_cover)
        self.BackToMainButton.clicked.connect(self.window.show_shelf)

    def load(self, book_id=None):
        """Подготовить страницу для добавления или редактирования."""
        self.book_id = book_id
        self.cover_image = ""
        self.ErrorText.clear()
        self.BookNameEdit.clear()
        self.AutorNameEdit.clear()
        self.CoverBookLabel.clear()
        self.CoverBookLabel.hide()
        self.set_cover_state(False)

        if book_id is None:
            self.ReadyButtonAddBook.setText("Добавить книгу")
            return
        self.ReadyButtonAddBook.setText("Сохранить изменения")
        book = storage.get_book(book_id)
        if book is None:
            return
        self.BookNameEdit.setText(book["name_book"])
        self.AutorNameEdit.setText(book["name_autor"])
        cover = book["cover"]
        if cover and paths.resolve(cover).is_file():
            self._show_cover(cover)
            self.cover_image = cover

    def ready_add_book(self):
        """Кнопка добавления/редактирования книги."""
        if self.BookNameEdit.text() == "" or self.AutorNameEdit.text() == "":
            self.ErrorText.setText("Заполните все окна!")
            return
        self.name_book = self.BookNameEdit.text()
        self.name_autor = self.AutorNameEdit.text()
        try:
            if self.book_id is not None:
                self._update_book()
            else:
                self._add_book()
        except Exception as error:
            QMessageBox.critical(
                self, "Ошибка", f"Не удалось сохранить книгу:\n{error}")
            return
        self.window.show_shelf()

    def _save_cover_copy(self, source, destination):
        with Image.open(source) as image:
            images.save_as_webp(image, paths.resolve(destination))
        return destination

    def _update_book(self):
        old_cover = storage.get_book(self.book_id)
        old_cover = old_cover["cover"] if old_cover else ""
        new_cover = old_cover
        relative = f'./data/covers/cover{self.book_id}.webp'

        if not self.cover_image:
            render_cover(self.name_book, self.name_autor,
                         paths.resolve(relative))
            new_cover = relative
        elif self.cover_image != old_cover:
            new_cover = self._save_cover_copy(self.cover_image, relative)

        if (old_cover and old_cover != new_cover
                and paths.resolve(old_cover).is_file()):
            try:
                paths.resolve(old_cover).unlink()
            except OSError:
                pass

        self.cover_image = new_cover
        storage.update_book(self.book_id, self.name_book,
                            self.name_autor, new_cover)

    def _add_book(self):
        book_id = storage.next_book_id()
        relative = f'./data/covers/cover{book_id}.webp'
        if self.cover_image:
            self._save_cover_copy(self.cover_image, relative)
        else:
            render_cover(self.name_book, self.name_autor,
                         paths.resolve(relative))
        self.cover_image = relative
        storage.add_book(self.name_book, self.name_autor, relative,
                         book_id=book_id)

    def get_cover(self):
        """Кнопка добавления обложки."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выбрать обложку", ".",
            "Изображения (*.webp *.jpg *.jpeg *.png *.bmp *.gif);;"
            "Все файлы (*)")
        if filename:
            self._show_cover(filename)
            self.cover_image = filename

    def _show_cover(self, path):
        """Показать обложку со скруглением и мягкой тенью."""
        self.filename = path
        pixmap = rounded_pixmap(
            QPixmap(str(paths.resolve(path))),
            (self.CoverBookLabel.width(), self.CoverBookLabel.height()),
            radius=14)
        self.CoverBookLabel.show()
        self.CoverBookLabel.setPixmap(pixmap)
        self.CoverBookLabel.setScaledContents(True)
        self.CoverBookLabel.setGraphicsEffect(
            QGraphicsDropShadowEffect(**cover_shadow()))
        self.set_cover_state(True)

    def set_cover_state(self, has_cover):
        """Переключение вида кнопки добавления обложки."""
        self.AddCoverButton.setText("" if has_cover else "Добавить обложку")
        self.AddCoverButton.setProperty("hasCover", has_cover)
        self.AddCoverButton.style().unpolish(self.AddCoverButton)
        self.AddCoverButton.style().polish(self.AddCoverButton)

    def on_theme_changed(self):
        if self.cover_image and paths.resolve(self.cover_image).is_file():
            self._show_cover(self.cover_image)
