import json

from designer.add_book_interface import Ui_Form
from designer.design import stylesheet

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PIL import Image, ImageDraw, ImageFont


class SecondForm(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./data/img/favicon.png'))
        self.setupUi(self)
        self.initUI()
        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def initUI(self):
        self.cover_image = ""
        self.ReadyButtonAddBook.clicked.connect(self.ready_add_book)
        self.AddCoverButton.clicked.connect(self.get_cover)
        self.BackToMainButton.clicked.connect(self.made)

    def ready_add_book(self):
        if self.BookNameEdit.text() != "" and self.AutorNameEdit.text() != "":
            # передаем значения автора и названия книги
            self.name_book = self.BookNameEdit.text()
            self.name_autor = self.AutorNameEdit.text()
            # добавляем к кол-ву книг +1
            self.data["count"] += 1
            # проверяем была ли добавлена обложка пользователем
            if self.cover_image == "":
                # вызываем функцию создания обложки
                self.create_cover()
            # добавляем значения в JSON
            self.data["books"].append({
                "name_book": self.name_book,
                "name_autor": self.name_autor,
                "cover": self.cover_image,
                "id": self.data["count"],
                "quotes": []})

            with open("./data/books-list.json", "w", encoding="utf-8") as write_file:
                json.dump(self.data, write_file, ensure_ascii=False)
            # сбрасываем значения
            self.cover_image = ""
            self.BookNameEdit.setText("")
            self.AutorNameEdit.setText("")
            self.ErrorText.setText("")
        else:
            self.ErrorText.setText("Заполните все окна!")

    def get_cover(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Выбрать обложку",
                                                         ".",
                                                         "JPEG Files(*.jpeg, *.jpg);;\
                             PNG Files(*.png)")
        # сохраняем обложку в папку с обложками
        if filename:
            img = Image.open(filename)
            path = f'./data/covers/cover{self.data["count"] + 1}.jpg'
            img.save(path)
            self.cover_image = path

    def create_cover(self):
        # создаем обложку с текстом
        im = Image.new('RGB', (120, 180), color=("rgb(60, 60, 60)"))
        draw_text = ImageDraw.Draw(im)
        # шрифт
        font = ImageFont.truetype('./data/font/Roboto-Black.ttf', size=14)
        # проверяем длину текста
        if len(self.name_book) > 12:
            name_book_img = f"{self.name_book[:12]}.."
        else:
            name_book_img = self.name_book
        # добавляем название книги на обложку
        draw_text.text(
            (5, 140),
            name_book_img,
            font=font,
            fill='rgb(240, 240, 240)')
        # шрифт
        font = ImageFont.truetype('./data/font/Roboto-Black.ttf', size=12)
        # проверяем длину текста
        if len(self.name_autor) > 14:
            name_autor_img = f"{self.name_autor[:14]}.."
        else:
            name_autor_img = self.name_autor
        # добавляем название книги на обложку
        draw_text.text(
            (5, 160),
            name_autor_img,
            font=font,
            fill='rgb(240, 240, 240)')
        # сохраняем
        path = f'./data/covers/cover{self.data["count"]}.jpg'
        im.save(path)
        self.cover_image = path

    def made(self):
        # выходим из окна и открываем main
        from interface.shelf import FirstForm
        self.close()
        self.ex = FirstForm()
        self.ex.setStyleSheet(stylesheet)
        self.ex.show()
