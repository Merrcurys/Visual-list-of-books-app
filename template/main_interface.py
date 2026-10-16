from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")

        self.Settings = QtWidgets.QPushButton(Form)
        self.Settings.setGeometry(QtCore.QRect(10, 10, 24, 24))
        self.Settings.setObjectName("Settings")

        self.ThemeButton = QtWidgets.QPushButton(Form)
        self.ThemeButton.setGeometry(QtCore.QRect(42, 10, 24, 24))
        self.ThemeButton.setObjectName("ThemeButton")

        self.SortButton = QtWidgets.QPushButton(Form)
        self.SortButton.setGeometry(QtCore.QRect(854, 10, 24, 24))
        self.SortButton.setObjectName("SortButton")

        self.PageNumber = QtWidgets.QLabel(Form)
        self.PageNumber.setGeometry(QtCore.QRect(792, 44, 81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(QtGui.QFont.Weight.Bold)
        self.PageNumber.setFont(font)
        self.PageNumber.setText("")
        self.PageNumber.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.PageNumber.setObjectName("PageNumber")

        self.SwipeLeftButton = QtWidgets.QPushButton(Form)
        self.SwipeLeftButton.setGeometry(QtCore.QRect(10, 566, 46, 30))
        self.SwipeLeftButton.setObjectName("SwipeLeftButton")

        self.SwipeRightButton = QtWidgets.QPushButton(Form)
        self.SwipeRightButton.setGeometry(QtCore.QRect(62, 566, 46, 30))
        self.SwipeRightButton.setObjectName("SwipeRightButton")

        self.AddBookButton = QtWidgets.QPushButton(Form)
        self.AddBookButton.setGeometry(QtCore.QRect(716, 566, 161, 30))
        self.AddBookButton.setObjectName("AddBookButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Визуальный список книг"))
        self.AddBookButton.setText(_translate("Form", "Добавить книгу"))
        self.SwipeLeftButton.setText(_translate("Form", "←"))
        self.SwipeRightButton.setText(_translate("Form", "→"))


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
