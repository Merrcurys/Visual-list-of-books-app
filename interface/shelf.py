import json
import os
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


class FirstForm(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./data/img/favicon.png'))
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # подключение кнопок
        self.AddBookButton.clicked.connect(self.add_book_form)
        self.Settings.clicked.connect(self.open_setting_form)

        # подключение кнопок для переключение страниц
        self.SwipeLeftButton.clicked.connect(self.swipe_left)
        self.SwipeRightButton.clicked.connect(self.swipe_right)

        # подключение кнопок кнопок для сортировки
        self.SortedIDButton.clicked.connect(
            lambda: self.sorted_by("id", "id"))
        self.SortedNameBookButton.clicked.connect(
            lambda: self.sorted_by("name_book", "name_autor"))
        self.SortedAutorButton.clicked.connect(
            lambda: self.sorted_by("name_autor", "name_book"))

        # значения для reverse
        self.id_count, self.autor_name_count, self.book_name_count = 1, 0, 0

        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # создаем список с количеством книг на каждой странице
            num_books = len(data['books'])
            self.pages = [[i * 8, min((i + 1) * 8, num_books)]
                          for i in range(math.ceil(num_books / 8))]

            self.page = 0  # номер страницы на главном экране

        # отображение кнопок перелистывания
        if len(self.pages) <= 1:
            self.SwipeLeftButton.hide()
            self.SwipeRightButton.hide()
        else:
            self.SwipeLeftButton.show()
            self.SwipeRightButton.show()

        if self.pages:
            pages = self.pages[self.page]
            self.display_books(pages[0], pages[1], ["id", "id", 0])

    def display_books(self, first, last, key):
        """Отображаем книги на странице."""
        self.book_list_id = []
        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.key = key
            print(self.key)
            data = sorted(data["books"], key=itemgetter(
                self.key[0], self.key[1]), reverse=self.key[2])

            # координаты и размер обложки
            cover_coords = {"x": 75, "y": 50, "w": 120, "h": 180}
            # координаты название автора
            autor_coords = {"x": 75, "y": 260, "w": 120, "h": 20}
            # координаты название книги
            bookname_coords = {"x": 75, "y": 240, "w": 120, "h": 20}

            for num in range(first, last):
                book = data[num]

                # создаем обложку книги
                self._create_cover_book(book, cover_coords)
                # создаем текст с названием книги
                self._create_bookname_text(book, bookname_coords)
                # создаем текст с фио автора
                self._create_author_text(book, autor_coords)

                # меняем координаты для слудующей книги
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
        self.cover_book.setStyleSheet("border: none;")
        self.cover_book.setGeometry(QtCore.QRect(
            cover_coords["x"], cover_coords["y"],
            cover_coords["w"], cover_coords["h"]))
        self.cover_book.clicked.connect(
            lambda: self.add_quote_form(book["id"]))

        self.book_list_id.append(self.cover_book_label)
        self.book_list_id.append(self.cover_book)

    def _create_bookname_text(self, book, bookname_coords):
        self.book_name = QLabel(self)
        # если название большое - сокращаем
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
        # если фио автора большое - сокращаем
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
            self.display_books(self.pages[self.page][0], self.pages[self.page][1], [
                key, secondary_key, order])
            self.show_books()

    def _toggle_sort(self, key):
        if key == "id":
            self.id_count = 1 - self.id_count
        elif key == "name_book":
            self.book_name_count = 1 - self.book_name_count
        elif key == "name_autor":
            self.autor_name_count = 1 - self.autor_name_count
        return self.id_count if key == "id" else self.book_name_count if key == "name_book" else self.autor_name_count

    def swipe_left(self):
        """Переключение на предыдущую страницу."""
        if self.pages:
            self.close_books()
            # циклический перенос
            self.page = (self.page - 1) % len(self.pages)
            self.display_books(self.pages[self.page]
                               [0], self.pages[self.page][1], self.key)
            self.show_books()

    def swipe_right(self):
        """Переключение на следующую страницу."""
        if self.pages:
            self.close_books()
            # циклический перенос
            self.page = (self.page - 1) % len(self.pages)
            self.display_books(self.pages[self.page]
                               [0], self.pages[self.page][1], self.key)
            self.show_books()
