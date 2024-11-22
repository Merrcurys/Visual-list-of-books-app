import json
import os
import zipfile
from pathlib import Path

from designer.settings_interface import Ui_Form
from designer.design import stylesheet

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QMessageBox
from PIL import Image, ImageDraw, ImageFont


class SettingsForm(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('./data/img/favicon.png'))
        self.setupUi(self)
        self.initUI()
        self.data_dir = Path("./data")
        with open(self.data_dir / "books-list.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def initUI(self):
        self.Export.clicked.connect(self.export_books)
        self.Import.clicked.connect(self.import_books)
        self.BackToMainButton.clicked.connect(self.made)

    def export_books(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Export Data", os.getcwd(
        ), "Zip Files (*.zip);;All Files (*)", options=options)

        if fileName:
            if not fileName.lower().endswith(".zip"):
                fileName += ".zip"

            try:
                with zipfile.ZipFile(fileName, 'w') as zipf:
                    img_dir = self.data_dir / "covers"
                    if img_dir.exists():
                        for root, _, files in os.walk(img_dir):
                            for file in files:
                                filepath = os.path.join(root, file)
                                if not os.path.splitext(file)[1]:
                                    file_with_ext = file + ".jpg"
                                    os.rename(filepath, os.path.join(
                                        root, file_with_ext))
                                    filepath = os.path.join(
                                        root, file_with_ext)
                                zipf.write(filepath, arcname=os.path.relpath(
                                    filepath, str(self.data_dir)))
                    if (self.data_dir / "books-list.json").exists():
                        zipf.write(self.data_dir / "books-list.json",
                                   arcname="books-list.json")

                QMessageBox.information(
                    self, "Успех", f"Данные успешно экспортированы в: {fileName}")
            except FileNotFoundError:
                QMessageBox.critical(
                    self, "Ошибка", "Не найдена папка 'data' или 'data/covers'.")
            except zipfile.BadZipFile:
                QMessageBox.critical(
                    self, "Ошибка", "Ошибка создания zip-архива.")
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Произошла неизвестная ошибка: {e}")

    def import_books(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Import Data", os.getcwd(
        ), "Zip Files (*.zip);;All Files (*)", options=options)

        if fileName:
            try:
                with zipfile.ZipFile(fileName, 'r') as zipf:
                    self.data_dir.mkdir(parents=True, exist_ok=True)
                    zipf.extractall(str(self.data_dir))

                with open(self.data_dir / "books-list.json", "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                QMessageBox.information(
                    self, "Успех", "Данные импортированы успешны!")

            except (FileNotFoundError, zipfile.BadZipFile, KeyError, json.JSONDecodeError) as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Ошибка в ипортировании данных: {e}")
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Во время импорта произошла непредвиденная ошибка: {e}")

    def made(self):
        from interface.shelf import FirstForm
        self.close()
        self.ex = FirstForm()
        self.ex.setStyleSheet(stylesheet)
        self.ex.show()