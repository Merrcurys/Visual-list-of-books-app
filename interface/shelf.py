import math
import os
from io import BytesIO

from core import paths, storage
from interface.add_book import cover_image
from template import icons
from template.animations import HoverScale
from template.design import (
    cover_shadow, get_theme, rounded_pixmap, theme_color)
from template.main_interface import Ui_Form

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QInputDialog, QMenu, QPushButton, QWidget, QLabel,
    QGraphicsDropShadowEffect)

SORT_OPTIONS = (
    ("id", "По времени добавления", "id"),
    ("name_book", "По названию книги", "name_autor"),
    ("name_autor", "По автору", "name_book"),
)


class ShelfPage(QWidget, Ui_Form):
    """Главная страница с полкой книг."""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.book_list_id = []
        self.cover_labels = []
        self.pages = []
        self.page = 0
        self.current_key = "id"
        self.current_secondary = "id"
        self.current_reverse = False
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.AddBookButton.clicked.connect(
            lambda: self.window.show_add_book())
        self.Settings.clicked.connect(self.window.show_settings)
        self.ThemeButton.clicked.connect(self.window.toggle_theme)
        self.SortButton.clicked.connect(self.show_sort_menu)
        self.SwipeLeftButton.clicked.connect(self.swipe_left)
        self.SwipeRightButton.clicked.connect(self.swipe_right)
        self._build_sort_menu()
        self._update_theme_button()

    # ------------------------------------------------------------------ тема
    def refresh_icons(self):
        color = theme_color("text_secondary")
        self.Settings.setIcon(icons.gear(color))
        self.ThemeButton.setIcon(
            icons.sun(color) if self._is_dark() else icons.moon(color))
        self.SortButton.setIcon(icons.filter_icon(color))
        for button in (self.Settings, self.ThemeButton, self.SortButton):
            button.setIconSize(QtCore.QSize(16, 16))

    def on_theme_changed(self):
        self.refresh_icons()
        for label in self.cover_labels:
            label.setGraphicsEffect(
                QGraphicsDropShadowEffect(**cover_shadow()))

    def _is_dark(self):
        return get_theme() == "dark"

    def _update_theme_button(self):
        self.ThemeButton.setToolTip(
            "Светлая тема" if self._is_dark() else "Тёмная тема")
        self.refresh_icons()

    # -------------------------------------------------------------- данные
    def reload(self):
        """Перечитать данные и построить полку заново."""
        self.close_books()
        (self.current_key, self.current_secondary,
         self.current_reverse) = storage.get_sort()

        num_books = storage.count_books()
        self.pages = [[i * 8, min((i + 1) * 8, num_books)]
                      for i in range(math.ceil(num_books / 8))]
        self.page = 0
        self.display_pagenumber()
        self.refresh_icons()
        self._update_sort_checks()

        if len(self.pages) <= 1:
            self.SwipeLeftButton.hide()
            self.SwipeRightButton.hide()
        else:
            self.SwipeLeftButton.show()
            self.SwipeRightButton.show()

        if self.pages:
            pages = self.pages[self.page]
            self.display_books(pages[0], pages[1])
            self.show_books()

    def display_pagenumber(self):
        count_pages = 1 if len(self.pages) == 0 else len(self.pages)
        self.PageNumber.setText(f"{self.page + 1}/{count_pages}")

    def display_books(self, first, last):
        """Отображаем книги на странице."""
        books = storage.get_books(
            self.current_key, self.current_secondary, self.current_reverse)

        cover_coords = {"x": 75, "y": 50, "w": 120, "h": 180}
        autor_coords = {"x": 75, "y": 260, "w": 120, "h": 20}
        bookname_coords = {"x": 75, "y": 240, "w": 120, "h": 20}

        for num in range(first, last):
            book = books[num]
            self._create_cover_book(book, cover_coords)
            self._create_bookname_text(book, bookname_coords)
            self._create_author_text(book, autor_coords)

            if (num + 1) % 4 == 0:
                cover_coords["x"], autor_coords["x"], bookname_coords["x"] = 75, 75, 75
                cover_coords["y"] += 250
                autor_coords["y"] += 250
                bookname_coords["y"] += 250
            else:
                cover_coords["x"] += 200
                autor_coords["x"] += 200
                bookname_coords["x"] += 200

    def _cover_pixmap(self, book):
        """Картинка обложки; для отсутствующей обложки — запасная."""
        pixmap = QPixmap(str(paths.resolve(book.get("cover", ""))))
        if not pixmap.isNull():
            return pixmap
        buffer = BytesIO()
        cover_image(
            book["name_book"], book["name_autor"]).save(
                buffer, format="WEBP", quality=90)
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue(), "WEBP")
        return pixmap

    def _create_cover_book(self, book, cover_coords):
        pixmap = rounded_pixmap(
            self._cover_pixmap(book),
            (cover_coords["w"], cover_coords["h"]), radius=12)
        self.cover_book_label = QLabel(self)
        self.cover_book_label.setPixmap(pixmap)
        self.cover_book_label.setScaledContents(True)
        self.cover_book_label.setGeometry(
            QtCore.QRect(
                cover_coords["x"], cover_coords["y"],
                cover_coords["w"], cover_coords["h"]))
        self.cover_book_label.setGraphicsEffect(
            QGraphicsDropShadowEffect(**cover_shadow()))

        self.cover_book = QPushButton(self)
        self.cover_book.setObjectName("coverOverlay")
        self.cover_book.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cover_book.setGeometry(QtCore.QRect(
            cover_coords["x"], cover_coords["y"],
            cover_coords["w"], cover_coords["h"]))
        self.cover_book.setToolTip(
            "ЛКМ — цитаты, ПКМ — изменить или удалить книгу")
        self.cover_book.clicked.connect(
            lambda: self.window.show_quote(book["id"]))
        self.cover_book.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.cover_book.customContextMenuRequested.connect(
            lambda position, b=book, w=self.cover_book:
            self.show_book_menu(b, w.mapToGlobal(position)))
        HoverScale([self.cover_book_label, self.cover_book], self.cover_book)

        self.book_list_id.append(self.cover_book_label)
        self.book_list_id.append(self.cover_book)
        self.cover_labels.append(self.cover_book_label)

    def _create_bookname_text(self, book, bookname_coords):
        self.book_name = QLabel(self)
        book_name = book["name_book"][:18] + \
            ".." if len(book["name_book"]) > 19 else book["name_book"]
        self.book_name.setText(book_name)
        self.book_name.setGeometry(QtCore.QRect(
            bookname_coords["x"], bookname_coords["y"],
            bookname_coords["w"], bookname_coords["h"]))
        self.book_name.setToolTip(book["name_book"])
        self.book_list_id.append(self.book_name)

    def _create_author_text(self, book, autor_coords):
        self.autor_name = QLabel(self)
        autor_name = book["name_autor"][:18] + \
            ".." if len(book["name_autor"]) > 19 else book["name_autor"]
        self.autor_name.setText(autor_name)
        self.autor_name.setGeometry(QtCore.QRect(
            autor_coords["x"], autor_coords["y"],
            autor_coords["w"], autor_coords["h"]))
        self.autor_name.setToolTip(book["name_autor"])
        self.book_list_id.append(self.autor_name)

    # ------------------------------------------------------- меню книги (ПКМ)
    def show_book_menu(self, book, global_position):
        menu = QMenu(self)
        edit_action = menu.addAction("Изменить книгу")
        delete_action = menu.addAction("Удалить книгу")
        chosen = menu.exec(global_position)
        if chosen is edit_action:
            self.window.show_add_book(book["id"])
        elif chosen is delete_action:
            self.confirm_delete_book(book)

    def confirm_delete_book(self, book):
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.InputMode.TextInput)
        dlg.setLabelText(
            f'Введите "удалить", чтобы удалить книгу "{book["name_book"]}":')
        dlg.setWindowTitle("Удаление книги")
        dlg.setOkButtonText("Удалить")
        dlg.setCancelButtonText("Отмена")
        dlg.resize(420, 100)
        if not dlg.exec():
            return
        if dlg.textValue().strip().lower() != "удалить":
            return
        cover = book.get("cover", "")
        storage.delete_book(book["id"])
        if cover and os.path.isfile(cover):
            try:
                os.remove(cover)
            except OSError:
                pass
        self.reload()

    def close_books(self):
        """Убрать книги текущей страницы."""
        for widget in self.book_list_id:
            widget.close()
            widget.deleteLater()
        self.book_list_id = []
        self.cover_labels = []

    def show_books(self):
        """Показать книги на странице."""
        for widget in self.book_list_id:
            widget.show()

    # ---------------------------------------------------------- сортировка
    def _build_sort_menu(self):
        self.sort_menu = QMenu(self)
        self.sort_menu.setMinimumWidth(240)
        self.sort_actions = {}
        self.sort_labels = {}
        for key, label, secondary in SORT_OPTIONS:
            action = QAction(label, self)
            action.triggered.connect(
                lambda checked, k=key, s=secondary: self.apply_sort(k, s))
            self.sort_menu.addAction(action)
            self.sort_actions[key] = action
            self.sort_labels[key] = label

    def show_sort_menu(self):
        self._update_sort_checks()
        position = self.SortButton.mapToGlobal(
            QtCore.QPoint(0, self.SortButton.height() + 4))
        self.sort_menu.exec(position)

    def _update_sort_checks(self):
        current = getattr(self, "current_key", "id")
        for key, action in self.sort_actions.items():
            prefix = "✓  " if key == current else "     "
            action.setText(prefix + self.sort_labels[key])

    def apply_sort(self, key, secondary_key):
        """Применить сортировку, выбранную в меню."""
        if key == self.current_key:
            reverse = storage.toggle_direction(key) == 1
        else:
            reverse = False
        storage.set_sort(key, secondary_key, reverse)
        self.current_key = key
        self.current_secondary = secondary_key
        self.current_reverse = reverse
        if self.pages:
            self.close_books()
            self.page = min(self.page, len(self.pages) - 1)
            self.display_books(
                self.pages[self.page][0], self.pages[self.page][1])
            self.show_books()
            self.display_pagenumber()
        self._update_sort_checks()

    # ------------------------------------------------------------- листание
    def swipe_left(self):
        """Переключение на предыдущую страницу."""
        if self.pages:
            self.close_books()
            self.page = (self.page - 1) % len(self.pages)
            self.display_books(self.pages[self.page]
                               [0], self.pages[self.page][1])
            self.display_pagenumber()
            self.show_books()

    def swipe_right(self):
        """Переключение на следующую страницу."""
        if self.pages:
            self.close_books()
            self.page = (self.page + 1) % len(self.pages)
            self.display_books(self.pages[self.page]
                               [0], self.pages[self.page][1])
            self.display_pagenumber()
            self.show_books()
