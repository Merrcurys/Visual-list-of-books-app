import json
import os

from template.add_quote_interface import Ui_Form
from template.design import stylesheet

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import (
    QMainWindow, QInputDialog, QLabel, QVBoxLayout, QFrame)


class QuoteCard(QFrame):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text  # Сохраняем текст цитаты
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                padding: 15px;
            }
            QLabel {
                color: #333;
                font-size: 16px;
                font-family: 'Roboto', sans-serif;
            }
        """)
        self.setup_ui(text)

        # Добавляем тень
        shadow = QGraphicsDropShadowEffect(
            blurRadius=10,
            xOffset=0,
            yOffset=2,
            color=QtGui.QColor(0, 0, 0, 50)
        )
        self.setGraphicsEffect(shadow)

        # Отслеживание кликов и выделений
        self.selection_in_progress = False

    def setup_ui(self, text):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.quote_label = QLabel(text)
        self.quote_label.setWordWrap(True)
        self.quote_label.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.quote_label.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard)

        # Устанавливаем обработчики событий для label
        self.quote_label.mousePressEvent = self.label_mouse_press
        self.quote_label.mouseReleaseEvent = self.label_mouse_release
        self.quote_label.mouseMoveEvent = self.label_mouse_move

        layout.addWidget(self.quote_label)

    def label_mouse_press(self, event):
        # Запоминаем начальную позицию для отслеживания выделения
        self.mouse_press_pos = event.pos()
        self.selection_in_progress = False
        # Передаем событие стандартному обработчику для QLabel
        QLabel.mousePressEvent(self.quote_label, event)

    def label_mouse_move(self, event):
        # Если мышь двигается после нажатия, значит выделяем текст
        if hasattr(self, 'mouse_press_pos') and (event.pos() - self.mouse_press_pos).manhattanLength() > 5:
            self.selection_in_progress = True
        # Передаем событие стандартному обработчику для QLabel
        QLabel.mouseMoveEvent(self.quote_label, event)

    def label_mouse_release(self, event):
        # Если не выделяли текст, обрабатываем как клик по карточке
        if not self.selection_in_progress and hasattr(self, 'click_handler'):
            self.click_handler(event, self.text)
        # Передаем событие стандартному обработчику для QLabel
        QLabel.mouseReleaseEvent(self.quote_label, event)
        # Сбрасываем флаг
        self.selection_in_progress = False

    def mousePressEvent(self, event):
        """Обработка нажатия мыши на карточку вне текста."""
        super().mousePressEvent(event)
        if hasattr(self, 'click_handler'):
            self.click_handler(event, self.text)


class Quote(QMainWindow, Ui_Form):
    def __init__(self, book_id):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./data/img/favicon.png'))
        self.book_id = book_id
        with open("./data/books-list.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.setupUi(self)
        self.quote_cards = []
        self.quotesLayout = self.quotesLayout  # Сохраняем ссылку на layout
        self.initUI()

    def initUI(self):
        self.AddQuoteButton.clicked.connect(self.dialog_add)
        self.ReadyButtonAddText.clicked.connect(self.made)
        self.DeletedBook.clicked.connect(self.book_del)
        self.DeletedBook.setToolTip(
            "Нажмите эту кнопку, чтобы удалить эту книгу.")
        self.DeletedQuote.setToolTip(
            "Выбирите цитату и нажмите на нее, а затем на эту кнопку, "
            "чтобы удалить.")
        self.DeletedQuote.clicked.connect(self.dialog_del)
        self.EditBookButton.clicked.connect(self.edit_book)
        self.EditBookButton.setToolTip(
            "Нажмите эту кнопку, чтобы изменить информацию о книге.")

        # добавляем цитаты из json-а
        for book in self.data["books"]:
            if book["id"] == self.book_id:
                for quot in book["quotes"]:
                    self.add_quote_card(quot)
                break

    def add_quote_card(self, text):
        """Добавляет карточку с цитатой."""
        card = QuoteCard(text)
        card.click_handler = self.select_quote
        self.quotesLayout.addWidget(card)
        self.quote_cards.append(card)

    def select_quote(self, event, text):
        """Выбирает цитату для удаления."""
        self.selected_quote = text
        # Снимаем выделение со всех карточек
        for card in self.quote_cards:
            card.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 10px;
                    padding: 15px;
                }
                QLabel {
                    color: #333;
                    font-size: 16px;
                    font-family: 'Roboto', sans-serif;
                }
            """)
        # Выделяем выбранную карточку
        for card in self.quote_cards:
            if card.findChild(QLabel).text() == text:
                card.setStyleSheet("""
                    QFrame {
                        background: #f0f0f0;
                        border-radius: 10px;
                        padding: 15px;
                    }
                    QLabel {
                        color: #333;
                        font-size: 16px;
                        font-family: 'Roboto', sans-serif;
                    }
                """)
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
            self.add_quote_card(name)
            self.ready()

    def dialog_del(self):
        """Диалоговое окно с удалением цитаты."""
        if hasattr(self, 'selected_quote'):
            dlg = QInputDialog(self)
            dlg.setInputMode(QInputDialog.TextInput)
            dlg.setLabelText('Введите "удалить", чтобы удалить цитату:')
            dlg.setWindowTitle("Подтверждение удаления цитаты")
            dlg.resize(400, 100)
            ok_pressed = dlg.exec_()
            name = dlg.textValue()

            if ok_pressed:
                if name.lower() == "удалить":
                    # Удаляем карточку
                    for card in self.quote_cards:
                        if card.findChild(QLabel).text() == self.selected_quote:
                            self.quotesLayout.removeWidget(card)
                            card.deleteLater()
                            self.quote_cards.remove(card)
                            break

                    # Удаляем из данных
                    for book in self.data["books"]:
                        if book["id"] == self.book_id:
                            book["quotes"].remove(self.selected_quote)
                            break

                    # Сохраняем изменения
                    with open("./data/books-list.json", "w", encoding="utf-8") as write_file:
                        json.dump(self.data, write_file, ensure_ascii=False)

                    # Сбрасываем выбранную цитату
                    if hasattr(self, 'selected_quote'):
                        delattr(self, 'selected_quote')

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
        # Собираем все цитаты из карточек
        quotes_list = []
        for card in self.quote_cards:
            quotes_list.append(card.findChild(QLabel).text())

        # Обновляем цитаты в данных
        for book in self.data["books"]:
            if book["id"] == self.book_id:
                book["quotes"] = quotes_list
                break

        # Сохраняем изменения
        with open("./data/books-list.json", "w", encoding="utf-8") as write_file:
            json.dump(self.data, write_file, ensure_ascii=False)

    def made(self):
        """Возвращение на домашнее окно."""
        from interface.shelf import FirstForm
        self.close()
        self.ex = FirstForm()
        self.ex.setStyleSheet(stylesheet)
        self.ex.show()

    def edit_book(self):
        """Редактирование информации о книге."""
        from interface.add_book import SecondForm
        self.close()
        self.edit_form = SecondForm(self.book_id)
        self.edit_form.setStyleSheet(stylesheet)
        # Заполняем поля текущими данными
        for book in self.data["books"]:
            if book["id"] == self.book_id:
                self.edit_form.BookNameEdit.setText(book["name_book"])
                self.edit_form.AutorNameEdit.setText(book["name_autor"])
                if os.path.isfile(book["cover"]):
                    pixmap = QPixmap(book["cover"])
                    self.edit_form.CoverBookLabel.show()
                    self.edit_form.CoverBookLabel.setPixmap(pixmap)
                    self.edit_form.CoverBookLabel.setScaledContents(True)
                    shadow = QGraphicsDropShadowEffect(
                        blurRadius=5, xOffset=4, yOffset=4)
                    self.edit_form.CoverBookLabel.setGraphicsEffect(shadow)
                    self.edit_form.cover_image = book["cover"]
                    self.edit_form.filename = book["cover"]
                    self.edit_form.AddCoverButton.setStyleSheet(
                        "border: none;")
                    self.edit_form.AddCoverButton.setText("")
                break
        self.edit_form.show()
