import json
import os

from template.add_quote_interface import Ui_Form
from template.design import stylesheet

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QInputDialog


class Quote(QMainWindow, Ui_Form):
    def __init__(self, book_id):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./data/img/favicon.png'))
        self.book_id = book_id
        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.AddQuoteButton.clicked.connect(self.dialog_add)
        self.ReadyButtonAddText.clicked.connect(self.made)
        self.DeletedBook.clicked.connect(self.book_del)
        self.DeletedBook.setToolTip(
            "Нажмите эту кнопку, чтобы удалить эту книгу.")
        self.DeletedQuote.setToolTip(
            "Выбирите цитату и нажмите на нее, а затем на эту кнопку, чтобы удалить.")
        self.DeletedQuote.clicked.connect(self.dialog_del)
        # добавляем цитаты из json-а в ListWidget
        for book in self.data["books"]:
            if book["id"] == self.book_id:
                for quot in book["quotes"]:
                    self.ListWidget.addItem(quot)
                break

    def dialog_add(self):
        """Диалоговое окно с добавлением цитаты."""
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText("Введите цитату:")
        dlg.setWindowTitle("Добавление цитаты")
        dlg.resize(400, 100)
        ok_pressed = dlg.exec_()
        name = dlg.textValue()
        if ok_pressed:
            self.ListWidget.addItem(name)
            self.ready()

    def dialog_del(self):
        """Диалоговое окно с удалением цитаты."""
        if self.ListWidget.currentItem() is not None:
            dlg = QInputDialog(self)
            dlg.setInputMode(QInputDialog.TextInput)
            dlg.setLabelText('Введите "удалить", чтобы удалить цитату:')
            dlg.setWindowTitle("Подтверждение удаления цитаты")
            dlg.resize(400, 100)
            ok_pressed = dlg.exec_()
            name = dlg.textValue()

            if ok_pressed:
                if name.lower() == "удалить":
                    # удаляем выбранный элемент из списка
                    item = self.ListWidget.currentItem()
                    if item is not None:
                        listItems = self.ListWidget.selectedItems()
                        if not listItems:
                            return
                        for item in listItems:
                            # узнаем название удаленного элемента
                            del_text = self.ListWidget.takeItem(
                                self.ListWidget.row(item)).text()
                            # удаляем
                            for book in self.data["books"]:
                                if book["id"] == self.book_id:
                                    book["quotes"].remove(del_text)
                            # перезаписываем json
                            with open("./data/books-list.json", "w", encoding="utf-8") as write_file:
                                json.dump(self.data, write_file,
                                          ensure_ascii=False)

    def book_del(self):
        """Диалоговое окно с удалением книги."""
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText('Введите "удалить", чтобы удалить книгу:')
        dlg.setWindowTitle("Подтверждение удаления книги")
        dlg.resize(400, 100)
        ok_pressed = dlg.exec_()
        name = dlg.textValue()

        if ok_pressed:
            if name.lower() == "удалить":
                # удаляем выбранный элемент из списка
                for book in self.data["books"]:
                    if book["id"] == self.book_id:
                        self.data["books"].remove(book)
                        # удаление обложки
                        if os.path.isfile(book["cover"]):
                            os.remove(book["cover"])
                        break
                # перезаписываем json
                with open("./data/books-list.json", "w", encoding="utf-8") as write_file:
                    json.dump(self.data, write_file, ensure_ascii=False)
                # выходим в shelf
                self.made()

    def ready(self):
        """Кнопка для добавления цитаты."""
        # добавляем в список цитаты из виджета
        quotes_list = []
        lw = self.ListWidget
        for quot in range(lw.count()):
            quotes_list.append(
                lw.item(quot).text())
        # проверка цитат из виджета и цитат из json-а
        for book in self.data["books"]:
            if book["id"] == self.book_id:
                if book["quotes"] != quotes_list:
                    # очищаем цитаты, для дальнейший перезаписи
                    book["quotes"].clear()
                    # добавляем цитаты в data
                    for quot in range(lw.count()):
                        book["quotes"].append(lw.item(quot).text())
        # перезаписываем json
        with open("./data/books-list.json", "w", encoding="utf-8") as write_file:
            json.dump(self.data, write_file, ensure_ascii=False)
        # чистим список цитат из виджета
        quotes_list.clear()

    def made(self):
        """Возвращение на домашнее окно."""
        from interface.shelf import FirstForm
        self.close()
        self.ex = FirstForm()
        self.ex.setStyleSheet(stylesheet)
        self.ex.show()
