from PyQt5.QtWidgets import QApplication
from interface.shelf import FirstForm
from template.design import stylesheet
import sys


def main():
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.setStyleSheet(stylesheet)
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
