import json
import os

from template.add_book_interface import Ui_Form
from template.design import stylesheet

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PIL import Image, ImageDraw, ImageFont


class SecondForm(QMainWindow, Ui_Form):
    def __init__(self, book_id=None):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./data/img/favicon.png'))
        self.setupUi(self)
        self.book_id = book_id
        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.initUI()

    def initUI(self):
        self.cover_image = ""
        self.ReadyButtonAddBook.clicked.connect(self.ready_add_book)
        self.AddCoverButton.clicked.connect(self.get_cover)
        self.BackToMainButton.clicked.connect(self.made)
        if self.book_id is not None:
            self.ReadyButtonAddBook.setText("Сохранить изменения")
            self.setWindowTitle("Редактирование книги")

    def ready_add_book(self):
        """Кнопка добавления/редактирования книги."""
        if self.BookNameEdit.text() != "" and self.AutorNameEdit.text() != "":
            # Передаем значения автора и названия книги
            self.name_book = self.BookNameEdit.text()
            self.name_autor = self.AutorNameEdit.text()

            if self.book_id is not None:
                # Редактирование существующей книги
                for book in self.data["books"]:
                    if book["id"] == self.book_id:
                        book["name_book"] = self.name_book
                        book["name_autor"] = self.name_autor
                        if not self.cover_image:
                            self._create_cover()
                            if os.path.isfile(book["cover"]):
                                os.remove(book["cover"])
                            book["cover"] = self.cover_image
                        elif self.cover_image != book["cover"]:
                            if os.path.isfile(book["cover"]):
                                os.remove(book["cover"])
                            # Сохраняем новую обложку
                            img = Image.open(self.cover_image)
                            path = f'./data/covers/cover{self.book_id}.jpg'
                            img.save(path)
                            book["cover"] = path
                        break
            else:
                # Добавление новой книги
                self.data["count"] += 1
                if not self.cover_image:
                    self._create_cover()
                else:
                    # Сохраняем новую обложку
                    img = Image.open(self.cover_image)
                    path = f'./data/covers/cover{self.data["count"]}.jpg'
                    img.save(path)
                    self.cover_image = path

                self.data["books"].append({
                    "name_book": self.name_book,
                    "name_autor": self.name_autor,
                    "cover": self.cover_image,
                    "id": self.data["count"],
                    "quotes": []})

            with open("./data/books-list.json", "w", encoding="utf-8") as write_file:
                json.dump(self.data, write_file, ensure_ascii=False)

            # Возвращаемся на главную
            self.made()
        else:
            self.ErrorText.setText("Заполните все окна!")

    def get_cover(self):
        """Кнопка добавления обложки."""
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать обложку",
                                                         ".",
                                                         "JPEG Files(*.jpeg, *.jpg);;\
                             PNG Files(*.png)")
        if filename:
            self.filename = filename
            # Показываем обложку
            pixmap = QPixmap(filename)
            self.CoverBookLabel.show()
            self.CoverBookLabel.setPixmap(pixmap)
            self.CoverBookLabel.setScaledContents(True)
            shadow = QGraphicsDropShadowEffect(
                blurRadius=5, xOffset=4, yOffset=4)
            self.CoverBookLabel.setGraphicsEffect(shadow)
            # Делаем кнопку прозрачной
            self.AddCoverButton.setStyleSheet("border: none;")
            self.AddCoverButton.setText("")
            # Сохраняем путь к выбранному файлу
            self.cover_image = filename

    def _create_cover(self):
        """Создание обложки."""
        # Создаем обложку с текстом
        im = Image.new('RGB', (120, 180), color=("rgb(60, 60, 60)"))
        draw_text = ImageDraw.Draw(im)
        # Подключаем шрифт
        font = ImageFont.truetype('./data/font/Roboto-Black.ttf', size=14)
        # Проверяем длину текста
        if len(self.name_book) > 12:
            name_book_img = f"{self.name_book[:12]}.."
        else:
            name_book_img = self.name_book
        # Добавляем название книги на обложку
        draw_text.text(
            (5, 140),
            name_book_img,
            font=font,
            fill='rgb(240, 240, 240)')
        # Подключаем шрифт
        font = ImageFont.truetype('./data/font/Roboto-Black.ttf', size=12)
        # Проверяем длину текста
        if len(self.name_autor) > 14:
            name_autor_img = f"{self.name_autor[:14]}.."
        else:
            name_autor_img = self.name_autor
        # Добавляем название книги на обложку
        draw_text.text(
            (5, 160),
            name_autor_img,
            font=font,
            fill='rgb(240, 240, 240)')
        # Сохраняем
        path = f'./data/covers/cover{self.data["count"]}.jpg'
        im.save(path)
        self.cover_image = path

    def made(self):
        """Возвращение на домашнее окно."""
        from interface.shelf import FirstForm
        self.close()
        self.ex = FirstForm()
        self.ex.setStyleSheet(stylesheet)
        self.ex.show()
