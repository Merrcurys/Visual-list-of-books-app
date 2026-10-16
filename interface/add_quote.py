from core import storage
from template.add_quote_interface import Ui_Form
from template.design import card_shadow

from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QWidget, QInputDialog, QLabel, QVBoxLayout, QFrame,
    QGraphicsDropShadowEffect)


class QuoteCard(QFrame):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text  # Сохраняем текст цитаты
        self.setObjectName("quoteCard")
        self.setProperty("selected", False)
        self.setup_ui(text)

        # Добавляем тень
        self.setGraphicsEffect(
            QGraphicsDropShadowEffect(**card_shadow()))

        # Отслеживание кликов и выделений
        self.selection_in_progress = False

    def set_selected(self, selected):
        """Подсветка выбранной карточки."""
        if self.property("selected") == selected:
            return
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def setup_ui(self, text):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        self.quote_label = QLabel(text)
        self.quote_label.setObjectName("quoteText")
        self.quote_label.setWordWrap(True)
        self.quote_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.quote_label.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
            | QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard)

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
            self.click_handler(event, self)
        # Передаем событие стандартному обработчику для QLabel
        QLabel.mouseReleaseEvent(self.quote_label, event)
        # Сбрасываем флаг
        self.selection_in_progress = False

    def mousePressEvent(self, event):
        """Обработка нажатия мыши на карточку вне текста."""
        super().mousePressEvent(event)
        if hasattr(self, 'click_handler'):
            self.click_handler(event, self)


class QuotePage(QWidget, Ui_Form):
    """Страница цитат выбранной книги."""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.book_id = None
        self.quote_cards = []
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.AddQuoteButton.clicked.connect(self.dialog_add)
        self.ReadyButtonAddText.clicked.connect(self.window.show_shelf)
        self.DeletedQuote.setToolTip(
            "Выберите цитату и нажмите на нее, а затем на эту кнопку, "
            "чтобы удалить.")
        self.DeletedQuote.clicked.connect(self.dialog_del)

    def load(self, book_id):
        """Загрузить цитаты книги."""
        self.book_id = book_id
        book = storage.get_book(book_id)

        for card in self.quote_cards:
            self.quotesLayout.removeWidget(card)
            card.deleteLater()
        self.quote_cards = []
        if hasattr(self, "selected_quote"):
            del self.selected_quote

        if book is not None:
            for quote in book["quotes"]:
                self.add_quote_card(quote)

    def add_quote_card(self, text):
        """Добавляет карточку с цитатой."""
        card = QuoteCard(text)
        card.click_handler = self.select_quote
        self.quotesLayout.addWidget(card)
        self.quote_cards.append(card)

    def select_quote(self, event, card):
        """Выбирает цитату для удаления."""
        self.selected_quote = card.text
        # Подсвечиваем только выбранную карточку
        for quote_card in self.quote_cards:
            quote_card.set_selected(quote_card is card)

    def dialog_add(self):
        """Диалоговое окно с добавлением цитаты."""
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.InputMode.TextInput)
        dlg.setLabelText("Введите цитату:")
        dlg.setWindowTitle("Добавление цитаты")
        dlg.setOkButtonText("Добавить")
        dlg.setCancelButtonText("Отмена")
        dlg.resize(400, 100)
        ok_pressed = dlg.exec()
        name = dlg.textValue()
        if ok_pressed and name.strip():
            self.add_quote_card(name)
            storage.add_quote(self.book_id, name)

    def dialog_del(self):
        """Диалоговое окно с удалением цитаты."""
        if not hasattr(self, 'selected_quote'):
            return
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.InputMode.TextInput)
        dlg.setLabelText('Введите "удалить", чтобы удалить цитату:')
        dlg.setWindowTitle("Подтверждение удаления цитаты")
        dlg.setOkButtonText("Удалить")
        dlg.setCancelButtonText("Отмена")
        dlg.resize(400, 100)
        ok_pressed = dlg.exec()
        name = dlg.textValue()

        if ok_pressed and name.lower() == "удалить":
            for card in self.quote_cards:
                if card.text == self.selected_quote:
                    self.quotesLayout.removeWidget(card)
                    card.deleteLater()
                    self.quote_cards.remove(card)
                    break
            storage.remove_quote(self.book_id, self.selected_quote)
            del self.selected_quote
