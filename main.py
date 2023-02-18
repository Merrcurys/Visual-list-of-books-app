from PyQt5.QtWidgets import QApplication
import sys
from interface.shelf import FirstForm
from designer.design import stylesheet


def main():
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.setStyleSheet(stylesheet)
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
