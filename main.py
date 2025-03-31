from PyQt5.QtWidgets import QApplication
from interface.shelf import FirstForm
from template.design import stylesheet
import sys
import os

# Отвечает за адаптивное расширение на 2-4к мониторах
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"


def main():
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.setStyleSheet(stylesheet)
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
