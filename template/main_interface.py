from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(887, 611)
        Form.setStyleSheet("")

        self.AddBookButton = QtWidgets.QPushButton(Form)
        self.AddBookButton.setGeometry(QtCore.QRect(770, 570, 101, 23))
        self.AddBookButton.setStyleSheet(
            "background: rgb(255, 255, 255); border-radius: 5px;")
        self.AddBookButton.setObjectName("AddBookButton")

        self.SwipeLeftButton = QtWidgets.QPushButton(Form)
        self.SwipeLeftButton.setGeometry(QtCore.QRect(10, 570, 51, 20))
        self.SwipeLeftButton.setStyleSheet(
            "background: rgb(255, 255, 255); border-radius: 5px;")
        self.SwipeLeftButton.setObjectName("SwipeLeftButton")

        self.SwipeRightButton = QtWidgets.QPushButton(Form)
        self.SwipeRightButton.setGeometry(QtCore.QRect(70, 570, 51, 20))
        self.SwipeRightButton.setStyleSheet(
            "background: rgb(255, 255, 255); border-radius: 5px;")
        self.SwipeRightButton.setObjectName("SwipeRightButton")

        self.SortedAutorButton = QtWidgets.QPushButton(Form)
        self.SortedAutorButton.setGeometry(QtCore.QRect(800, 10, 21, 20))
        self.SortedAutorButton.setStyleSheet(
            "background: rgb(255, 255, 255); border-radius: 10px;")
        self.SortedAutorButton.setObjectName("SortedAutorButton")
        self.SortedAutorButton.setToolTip(
            "Сортировка по автору.")

        self.SortedNameBookButton = QtWidgets.QPushButton(Form)
        self.SortedNameBookButton.setGeometry(QtCore.QRect(830, 10, 21, 20))
        self.SortedNameBookButton.setStyleSheet(
            "background: rgb(255, 255, 255); border-radius: 10px;")
        self.SortedNameBookButton.setObjectName("SortedNameBookButton")
        self.SortedNameBookButton.setToolTip(
            "Сортировка по названию книги.")

        self.SortedIDButton = QtWidgets.QPushButton(Form)
        self.SortedIDButton.setGeometry(QtCore.QRect(860, 10, 21, 20))
        self.SortedIDButton.setStyleSheet(
            "background: rgb(255, 255, 255); border-radius: 10px;")
        self.SortedIDButton.setObjectName("SortedIDButton")
        self.SortedIDButton.setToolTip(
            "Сортировка по времени добавления.")

        self.Settings = QtWidgets.QPushButton(Form)
        self.Settings.setGeometry(QtCore.QRect(10, 10, 21, 20))
        self.Settings.setStyleSheet(
            "background: rgb(255, 255, 255); border-radius: 10px;")
        self.Settings.setText("")
        self.Settings.setObjectName("Settings")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Визуальный список книг"))
        self.AddBookButton.setText(_translate("Form", "Добавить книгу"))
        self.SwipeLeftButton.setText(_translate("Form", "←"))
        self.SwipeRightButton.setText(_translate("Form", "→"))
        self.SortedAutorButton.setText(_translate("Form", "А"))
        self.SortedNameBookButton.setText(_translate("Form", "Н"))
        self.SortedIDButton.setText(_translate("Form", "П"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
