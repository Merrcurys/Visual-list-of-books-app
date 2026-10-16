import os

from core import storage
from template import icons
from template.design import theme_color
from template.settings_interface import Ui_Form

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox


class SettingsPage(QWidget, Ui_Form):
    """Страница настроек с экспортом и импортом данных."""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.ExportCard.clicked.connect(self.export_books)
        self.ImportCard.clicked.connect(self.import_books)
        self.BackToMainButton.clicked.connect(self.window.show_shelf)
        self.refresh_icons()

    def refresh_icons(self):
        color = theme_color("accent")
        size = QtCore.QSize(44, 44)
        self.ExportCard.Icon.setPixmap(
            icons.export_icon(color).pixmap(size))
        self.ImportCard.Icon.setPixmap(
            icons.import_icon(color).pixmap(size))

    def on_theme_changed(self):
        self.refresh_icons()

    def load(self):
        """Обновить состояние страницы перед показом."""
        self.refresh_icons()

    def export_books(self):
        """Экспорт библиотеки в архив (.zip) или базу данных (.db)."""
        default_filename = os.path.join(
            os.getcwd(), "book_tracker_backup.zip")
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", default_filename,
            "Архив ZIP (*.zip);;База данных (*.db);;Все файлы (*)")

        if not file_name:
            return
        try:
            if file_name.lower().endswith(".db"):
                storage.export_database(file_name)
            else:
                if not file_name.lower().endswith(".zip"):
                    file_name += ".zip"
                storage.export_archive(file_name)
            self._info("Данные успешно экспортированы в:\n" + file_name)
        except Exception as e:
            self._error(f"Не удалось экспортировать данные: {e}")

    def import_books(self):
        """Импорт библиотеки из архива (.zip) или базы данных (.db)."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Импорт данных", os.getcwd(),
            "База данных или архив (*.db *.zip);;Все файлы (*)")

        if not file_name:
            return
        try:
            storage.import_data(file_name)
            self._info("Данные успешно импортированы.")
        except Exception as e:
            self._error(f"Не удалось импортировать данные: {e}")

    def _info(self, message):
        """Информационный диалог с русской кнопкой."""
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Information)
        box.setWindowTitle("Успех")
        box.setText(message)
        box.addButton("Понятно", QMessageBox.ButtonRole.AcceptRole)
        box.exec()

    def _error(self, message):
        """Диалог ошибки с русской кнопкой."""
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Critical)
        box.setWindowTitle("Ошибка")
        box.setText(message)
        box.addButton("Понятно", QMessageBox.ButtonRole.AcceptRole)
        box.exec()
