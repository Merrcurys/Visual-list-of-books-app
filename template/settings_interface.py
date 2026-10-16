from PyQt6 import QtCore, QtWidgets


class SettingsCard(QtWidgets.QFrame):
    """Кликабельная карточка раздела настроек."""

    clicked = QtCore.pyqtSignal()

    def __init__(self, title, text, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsCard")
        self.setFixedSize(300, 230)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(12)

        self.Icon = QtWidgets.QLabel()
        self.Icon.setObjectName("cardIcon")
        self.Icon.setFixedSize(56, 56)
        self.Icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.Title = QtWidgets.QLabel(title)
        self.Title.setObjectName("cardTitle")

        self.Text = QtWidgets.QLabel(text)
        self.Text.setObjectName("cardText")
        self.Text.setWordWrap(True)
        self.Text.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop
                               | QtCore.Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.Icon)
        layout.addWidget(self.Title)
        layout.addWidget(self.Text)
        layout.addStretch()

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.MouseButton.LeftButton
                and self.rect().contains(event.position().toPoint())):
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")

        root = QtWidgets.QVBoxLayout(Form)
        root.setContentsMargins(40, 36, 40, 30)
        root.setSpacing(8)

        self.SettingsName = QtWidgets.QLabel("НАСТРОЙКИ")
        self.SettingsName.setObjectName("SettingsName")
        self.SettingsName.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(self.SettingsName)

        self.SettingsSubtitle = QtWidgets.QLabel(
            "Сохраните библиотеку одним архивом или восстановите её из копии")
        self.SettingsSubtitle.setObjectName("SettingsSubtitle")
        self.SettingsSubtitle.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter)
        root.addWidget(self.SettingsSubtitle)

        root.addSpacing(28)

        cards = QtWidgets.QHBoxLayout()
        cards.setSpacing(28)
        cards.addStretch()
        self.ExportCard = SettingsCard(
            "Экспорт",
            "Сохраняет книги, цитаты и обложки в архив ZIP или в файл "
            "базы данных SQLite для переноса на другой компьютер.")
        self.ImportCard = SettingsCard(
            "Импорт",
            "Загружает библиотеку из архива ZIP или базы данных, "
            "заменяя текущие книги и цитаты.")
        cards.addWidget(self.ExportCard)
        cards.addWidget(self.ImportCard)
        cards.addStretch()
        root.addLayout(cards)

        root.addStretch()

        self.BackToMainButton = QtWidgets.QPushButton("На главную")
        self.BackToMainButton.setObjectName("BackToMainButton")
        root.addWidget(self.BackToMainButton,
                       alignment=QtCore.Qt.AlignmentFlag.AlignLeft)


if __name__ == "__main__":
    import sys
    from template.design import apply_theme
    app = QtWidgets.QApplication(sys.argv)
    apply_theme(app)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
