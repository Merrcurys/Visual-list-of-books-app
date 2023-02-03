import sys
import json
from operator import itemgetter

from add_book import SecondForm
from add_quote import Quote
from design import stylesheet
import main_interface

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap


class FirstForm(QMainWindow, main_interface.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('design/favicon.png'))
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.AddBookButton.clicked.connect(self.AddBookForm)
        # кнопки для переключение страниц
        self.SwipeLeftButton.clicked.connect(self.SwipeLeft)
        self.SwipeRightButton.clicked.connect(self.SwipeRight)
        # кнопки для сортировки
        self.SortedIDButton.clicked.connect(self.SortedID)
        self.SortedNameBookButton.clicked.connect(self.SortedNameBook)
        self.SortedAutorButton.clicked.connect(self.SortedAutor)
        # подсказки
        self.SortedIDButton.setToolTip(
            "Сортировка по времени добавления.")
        self.SortedNameBookButton.setToolTip(
            "Сортировка по названию книги.")
        self.SortedAutorButton.setToolTip(
            "Сортировка по автору.")

        with open("books-list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # создаем список с номерами книг на каждой странице
            self.pages = []
            first, last = 0, 8
            for _ in range(len(data['books']) // 8):
                self.pages.append([first, last])
                first += 8
                last += 8
            if len(data['books']) % 8 != 0:
                last = len(data['books'])
                self.pages.append([first, last])

            self.page = 0  # номер страницы на главном экране

        if self.pages:
            self.DisplayBooks(self.pages[self.page]
                              [0], self.pages[self.page][1], "id")

    def DisplayBooks(self, first, last, key):  # отображаем страницу с книгами
        self.book_list_id = []
        with open("books-list.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.key = key
            data = sorted(data["books"], key=itemgetter(self.key))
            # координаты и размер обложки
            x_cover, y_cover, wh_cover, hh_cover = 75, 50, 120, 180
            # координаты название книги
            x_autor, y_autor, wh_autor, hh_autor = 75, 260, 120, 20
            # координаты название автора
            x_book, y_book, wh_book, hh_book = 75, 240, 120, 20

            for num in range(first, last):
                book = data[num]
                # добавляем обложку
                self.cover_book_label = QLabel(self)
                pixmap = QPixmap(book["cover"])
                self.cover_book_label.setPixmap(pixmap)
                self.cover_book_label.setScaledContents(True)
                self.cover_book_label.setGeometry(
                    QtCore.QRect(x_cover, y_cover, wh_cover, hh_cover))
                self.book_list_id.append(self.cover_book_label)
                # добавляем кнопку вниз обложки
                self.cover_book = QPushButton(self)
                self.cover_book.clicked.connect(self.AddQuoteForm)
                self.cover_book.setStyleSheet("border: none;")
                self.cover_book.setGeometry(
                    QtCore.QRect(x_cover, y_cover, wh_cover, hh_cover))
                self.connectButton(
                    self.cover_book, self.AddQuoteForm, book["id"])
                self.book_list_id.append(self.cover_book)
                # добавляем название
                self.book_name = QLabel(self)
                # если название большое - сокращаем
                if len(book["name_book"]) > 19:
                    self.book_name.setText(f'{book["name_book"][:18]}..')
                else:
                    self.book_name.setText(book["name_book"])
                self.book_name.setGeometry(QtCore.QRect(
                    x_book, y_book, wh_book, hh_book))
                self.book_name.setToolTip(book["name_book"])
                self.book_list_id.append(self.book_name)
                # добавляем автора
                self.autor_name = QLabel(self)
                # если название большое - сокращаем
                if len(book["name_autor"]) > 19:
                    self.autor_name.setText(f'{book["name_autor"][:18]}..')
                else:
                    self.autor_name.setText(book["name_autor"])
                self.autor_name.setGeometry(QtCore.QRect(
                    x_autor, y_autor, wh_autor, hh_autor))
                self.autor_name.setToolTip(book["name_autor"])
                self.book_list_id.append(self.autor_name)
                # меняем координаты для слудующей книги
                if (num + 1) % 4 == 0:
                    x_cover, x_autor, x_book = 75, 75, 75
                    y_cover += 250
                    y_autor += 250
                    y_book += 250
                else:
                    x_cover += 200
                    x_autor += 200
                    x_book += 200

    def CloseBooks(self):  # закрываем все виджеты книг
        if self.book_list_id:
            for widget in self.book_list_id:
                widget.close()

    def ShowBooks(self):  # показываем все виджеты книг
        if self.book_list_id:
            for widget in self.book_list_id:
                widget.show()

    def connectButton(self, button, QuoteForm, book_id):  # передаем id в AddQuoteForm
        button.clicked.connect(lambda: QuoteForm(book_id))

    def AddBookForm(self):  # открываем окно с добавлением книг
        self.second_form = SecondForm()
        self.second_form.setStyleSheet(stylesheet)
        self.second_form.show()
        self.close()

    def AddQuoteForm(self, book_id):  # открываем окно с добавлением цитат
        self.quote_form = Quote(book_id)
        self.quote_form.setStyleSheet(stylesheet)
        self.quote_form.show()
        self.close()

    def SortedID(self):  # сортировка по ID
        if self.pages:
            self.CloseBooks()
            self.DisplayBooks(self.pages[self.page][0],
                              self.pages[self.page][1], "id")
            self.ShowBooks()

    def SortedNameBook(self):  # сортировка по названию книги
        if self.pages:
            self.CloseBooks()
            self.DisplayBooks(self.pages[self.page][0],
                              self.pages[self.page][1], "name_book")
            self.ShowBooks()

    def SortedAutor(self):  # сортировка по автору
        if self.pages:
            self.CloseBooks()
            self.DisplayBooks(self.pages[self.page][0],
                              self.pages[self.page][1], "name_autor")
            self.ShowBooks()

    def SwipeLeft(self):  # прошлая страница
        if self.pages:
            self.CloseBooks()
            # зацикливаем список страниц
            if self.page - 1 < 0:
                self.page = len(self.pages) - 1
            else:
                self.page -= 1
            self.DisplayBooks(self.pages[self.page][0],
                              self.pages[self.page][1], self.key)
            self.ShowBooks()

    def SwipeRight(self):  # следующая страница
        if self.pages:
            self.CloseBooks()
            # зацикливаем список страниц
            if self.page + 1 > len(self.pages) - 1:
                self.page = 0
            else:
                self.page += 1
            self.DisplayBooks(self.pages[self.page][0],
                              self.pages[self.page][1], self.key)
            self.ShowBooks()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.setStyleSheet(stylesheet)
    ex.show()
    sys.exit(app.exec())
    
