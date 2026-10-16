from PyQt6.QtCore import QLibraryInfo, QLocale, QTranslator
from PyQt6.QtWidgets import QApplication
from interface.main_window import MainWindow
from template.design import apply_theme
import sys


def install_russian(app):
    """Русские подписи в стандартных диалогах Qt."""
    QLocale.setDefault(QLocale(QLocale.Language.Russian,
                               QLocale.Country.Russia))
    translator = QTranslator(app)
    path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    if translator.load("qtbase_ru", path):
        app.installTranslator(translator)
    return translator


def main():
    app = QApplication(sys.argv)
    app._translator = install_russian(app)
    apply_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
