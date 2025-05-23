from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")

        self.ReadyButtonAddBook = QtWidgets.QPushButton(Form)
        self.ReadyButtonAddBook.setGeometry(QtCore.QRect(490, 410, 151, 21))
        self.ReadyButtonAddBook.setStyleSheet(
            "font-size: 12px;  background: rgb(255, 255, 255); border-radius: 5px;")
        self.ReadyButtonAddBook.setObjectName("ReadyButtonAddBook")

        self.BookName = QtWidgets.QLabel(Form)
        self.BookName.setGeometry(QtCore.QRect(300, 280, 141, 21))
        self.BookName.setStyleSheet("font-size: 18px; ")
        self.BookName.setObjectName("BookName")

        self.AutorName = QtWidgets.QLabel(Form)
        self.AutorName.setGeometry(QtCore.QRect(300, 330, 141, 21))
        self.AutorName.setStyleSheet("font-size: 18px; ")
        self.AutorName.setObjectName("AutorName")

        self.CoverBookLabel = QLabel(self)
        self.CoverBookLabel.setGeometry(QtCore.QRect(83, 160, 180, 270))

        self.AddCoverButton = QtWidgets.QPushButton(Form)
        self.AddCoverButton.setGeometry(QtCore.QRect(83, 160, 180, 265))
        self.AddCoverButton.setStyleSheet("background: rgb(255, 255, 255);")
        self.AddCoverButton.setObjectName("AddCoverButton")

        self.BookNameEdit = QtWidgets.QLineEdit(Form)
        self.BookNameEdit.setGeometry(QtCore.QRect(450, 270, 291, 41))
        self.BookNameEdit.setStyleSheet("font-size: 18px; ")
        self.BookNameEdit.setObjectName("BookNameEdit")

        self.AutorNameEdit = QtWidgets.QLineEdit(Form)
        self.AutorNameEdit.setGeometry(QtCore.QRect(450, 320, 291, 41))
        self.AutorNameEdit.setStyleSheet("font-size: 18px; ")
        self.AutorNameEdit.setObjectName("AutorNameEdit")

        self.ErrorText = QtWidgets.QLabel(Form)
        self.ErrorText.setGeometry(QtCore.QRect(510, 220, 191, 41))
        self.ErrorText.setStyleSheet("font-size: 18px; ")
        self.ErrorText.setText("")
        self.ErrorText.setObjectName("ErrorText")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 440, 91, 16))
        self.label.setStyleSheet("font-size: 10px; ")
        self.label.setObjectName("label")

        self.BackToMainButton = QtWidgets.QPushButton(Form)
        self.BackToMainButton.setGeometry(QtCore.QRect(10, 581, 71, 20))
        self.BackToMainButton.setStyleSheet(
            "font-size: 12px;  background: rgb(255, 255, 255); border-radius: 5px;")
        self.BackToMainButton.setObjectName("BackToMainButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавление книги"))
        self.ReadyButtonAddBook.setText(_translate("Form", "Готово"))
        self.BookName.setText(_translate("Form", "Название книги"))
        self.AutorName.setText(_translate("Form", "Автор"))
        self.AddCoverButton.setText(_translate("Form", "Добавить обложку"))
        self.label.setText(_translate("Form", "*не обязательно"))
        self.BackToMainButton.setText(_translate("Form", "Назад"))
