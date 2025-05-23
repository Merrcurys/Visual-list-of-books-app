import json
import math
from operator import itemgetter

from interface.add_book import SecondForm
from interface.add_quote import Quote
from interface.setting import SettingsForm
from template.design import stylesheet
from template.main_interface import Ui_Form

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt


class FirstForm(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./data/img/favicon.png'))
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # Подключение кнопок
        self.AddBookButton.clicked.connect(self.add_book_form)
        self.Settings.clicked.connect(self.open_setting_form)

        # Подключение кнопок для переключение страниц
        self.SwipeLeftButton.clicked.connect(self.swipe_left)
        self.SwipeRightButton.clicked.connect(self.swipe_right)

        # Подключение кнопок кнопок для сортировки
        self.SortedIDButton.clicked.connect(
            lambda: self.sorted_by("id", "id"))
        self.SortedNameBookButton.clicked.connect(
            lambda: self.sorted_by("name_book", "name_autor"))
        self.SortedAutorButton.clicked.connect(
            lambda: self.sorted_by("name_autor", "name_book"))

        # Подсказки
        self.SortedIDButton.setToolTip(
            "Сортировка по времени добавления.")
        self.SortedNameBookButton.setToolTip(
            "Сортировка по названию книги.")
        self.SortedAutorButton.setToolTip(
            "Сортировка по автору.")

        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Значения для reverse
            self.id_count, self.autor_name_count, self.book_name_count = data["sort"]["digit"]

            # Создаем список с количеством книг на каждой странице
            num_books = len(data['books'])
            self.pages = [[i * 8, min((i + 1) * 8, num_books)]
                          for i in range(math.ceil(num_books / 8))]

            self.page = 0  # Номер страницы на главном экране
            self.display_pagenumber()

        # Отображение кнопок перелистывания
        if len(self.pages) <= 1:
            self.SwipeLeftButton.hide()
            self.SwipeRightButton.hide()
        else:
            self.SwipeLeftButton.show()
            self.SwipeRightButton.show()

        if self.pages:
            pages = self.pages[self.page]
            self.display_books(pages[0], pages[1])

    def display_pagenumber(self):
        count_pages = 1 if len(self.pages) == 0 else len(self.pages)
        self.PageNumber.setText(f"{self.page + 1}/{count_pages}")

    def display_books(self, first, last):
        """Отображаем книги на странице."""
        self.book_list_id = []
        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.key = data["sort"]["text"]
            data = sorted(data["books"], key=itemgetter(
                self.key[0], self.key[1]), reverse=self.key[2])

            # Координаты и размер обложки
            cover_coords = {"x": 75, "y": 50, "w": 120, "h": 180}
            # Координаты название автора
            autor_coords = {"x": 75, "y": 260, "w": 120, "h": 20}
            # Координаты название книги
            bookname_coords = {"x": 75, "y": 240, "w": 120, "h": 20}

            for num in range(first, last):
                book = data[num]

                # Создаем обложку книги
                self._create_cover_book(book, cover_coords)
                # Создаем текст с названием книги
                self._create_bookname_text(book, bookname_coords)
                # Создаем текст с фио автора
                self._create_author_text(book, autor_coords)

                # Меняем координаты для слудующей книги
                if (num + 1) % 4 == 0:
                    cover_coords["x"], autor_coords["x"], bookname_coords["x"] = 75, 75, 75
                    cover_coords["y"] += 250
                    autor_coords["y"] += 250
                    bookname_coords["y"] += 250
                else:
                    cover_coords["x"] += 200
                    autor_coords["x"] += 200
                    bookname_coords["x"] += 200

    def _create_cover_book(self, book, cover_coords):
        pixmap = QPixmap(book["cover"])
        self.cover_book_label = QLabel(self)
        self.cover_book_label.setPixmap(pixmap)
        self.cover_book_label.setScaledContents(True)
        self.cover_book_label.setGeometry(
            QtCore.QRect(
                cover_coords["x"], cover_coords["y"],
                cover_coords["w"], cover_coords["h"]))
        shadow = QGraphicsDropShadowEffect(
            blurRadius=5, xOffset=4, yOffset=4)
        self.cover_book_label.setGraphicsEffect(shadow)

        self.cover_book = QPushButton(self)
        # Установка курсора для hover
        self.cover_book.setCursor(Qt.PointingHandCursor)
        self.cover_book.setGeometry(QtCore.QRect(
            cover_coords["x"], cover_coords["y"],
            cover_coords["w"], cover_coords["h"]))
        self.cover_book.clicked.connect(
            lambda: self.add_quote_form(book["id"]))

        # Установка hover эффекта
        self.cover_book.setStyleSheet(
            """
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 50);
                border: 1px solid #000;
            }
            """
        )

        self.book_list_id.append(self.cover_book_label)
        self.book_list_id.append(self.cover_book)

    def _create_bookname_text(self, book, bookname_coords):
        self.book_name = QLabel(self)
        # Если название большое - сокращаем
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
        # Если фио автора большое - сокращаем
        autor_name = book["name_autor"][:18] + \
            ".." if len(book["name_autor"]
                        ) > 19 else book["name_autor"]
        self.autor_name.setText(autor_name)
        self.autor_name.setGeometry(QtCore.QRect(
            autor_coords["x"], autor_coords["y"],
            autor_coords["w"], autor_coords["h"]))
        self.autor_name.setToolTip(book["name_autor"])
        self.book_list_id.append(self.autor_name)

    def close_books(self):
        """Закрытие книг на странице."""
        if self.book_list_id:
            for widget in self.book_list_id:
                widget.close()

    def show_books(self):
        """Отображение книг на странице."""
        if self.book_list_id:
            for widget in self.book_list_id:
                widget.show()

    def add_book_form(self):
        """Открытие окно с добавлением книг."""
        self.second_form = SecondForm()
        self.second_form.setStyleSheet(stylesheet)
        self.second_form.show()
        self.close()

    def add_quote_form(self, book_id):
        """Открытие окно с добавлением цитат у книги."""
        self.quote_form = Quote(book_id)
        self.quote_form.setStyleSheet(stylesheet)
        self.quote_form.show()
        self.close()

    def open_setting_form(self):
        """Открытие окно с настройками."""
        self.settings_form = SettingsForm()
        self.settings_form.setStyleSheet(stylesheet)
        self.settings_form.show()
        self.close()

    def sorted_by(self, key, secondary_key):
        """Сортировка книг на экране."""
        if self.pages:
            self.close_books()
            order = self._toggle_sort(key)

            # Перезаписываем значения сортировки
            with open("./data/books-list.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                data["sort"]["text"] = [key, secondary_key, order]

            with open("./data/books-list.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            self.display_books(
                self.pages[self.page][0], self.pages[self.page][1])
            self.show_books()

    def _toggle_sort(self, key):
        if key == "id":
            self.id_count = 1 - self.id_count
        elif key == "name_book":
            self.book_name_count = 1 - self.book_name_count
        elif key == "name_autor":
            self.autor_name_count = 1 - self.autor_name_count

        # Перезаписываем значения для reverse
        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            data["sort"]["digit"] = [self.id_count,
                                     self.autor_name_count, self.book_name_count]

        with open("./data/books-list.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        return self.id_count if key == "id" else self.book_name_count if key == "name_book" else self.autor_name_count

    def swipe_left(self):
        """Переключение на предыдущую страницу."""
        if self.pages:
            self.close_books()
            # Циклический перенос
            self.page = (self.page - 1) % len(self.pages)
            self.display_books(self.pages[self.page]
                               [0], self.pages[self.page][1])
            self.display_pagenumber()
            self.show_books()

    def swipe_right(self):
        """Переключение на следующую страницу."""
        if self.pages:
            self.close_books()
            # Циклический перенос
            self.page = (self.page + 1) % len(self.pages)
            self.display_books(self.pages[self.page]
                               [0], self.pages[self.page][1])
            self.display_pagenumber()
            self.show_books()
