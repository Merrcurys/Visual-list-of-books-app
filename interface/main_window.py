"""Единое окно приложения с переключением страниц через QStackedWidget."""

from PyQt6 import QtGui
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from interface.add_book import AddBookPage
from interface.add_quote import QuotePage
from interface.setting import SettingsPage
from interface.shelf import ShelfPage
from template.design import apply_theme, background_pixmap, toggle_theme


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./data/img/favicon.png'))
        self.setFixedSize(887, 611)

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.shelf_page = ShelfPage(self)
        self.add_book_page = AddBookPage(self)
        self.quote_page = QuotePage(self)
        self.settings_page = SettingsPage(self)
        for page in (self.shelf_page, self.add_book_page,
                     self.quote_page, self.settings_page):
            self.stack.addWidget(page)

        self.show_shelf()

    def show_shelf(self):
        self.shelf_page.reload()
        self._show(self.shelf_page, "Визуальный список книг")

    def show_add_book(self, book_id=None):
        self.add_book_page.load(book_id)
        self._show(self.add_book_page,
                   "Редактирование книги" if book_id is not None
                   else "Добавление книги")

    def show_quote(self, book_id):
        self.quote_page.load(book_id)
        self._show(self.quote_page, "Цитаты книги")

    def show_settings(self):
        self.settings_page.load()
        self._show(self.settings_page, "Настройки")

    def toggle_theme(self):
        toggle_theme()
        apply_theme(QApplication.instance())
        self.shelf_page.on_theme_changed()
        self.settings_page.on_theme_changed()
        self.add_book_page.on_theme_changed()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, background_pixmap(self.size()))
        painter.end()

    def _show(self, page, title):
        self.stack.setCurrentWidget(page)
        self.setWindowTitle(title)
