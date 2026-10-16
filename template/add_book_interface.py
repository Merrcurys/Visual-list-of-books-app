from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QLabel


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")

        self.ReadyButtonAddBook = QtWidgets.QPushButton(Form)
        self.ReadyButtonAddBook.setGeometry(QtCore.QRect(490, 410, 211, 34))
        self.ReadyButtonAddBook.setObjectName("ReadyButtonAddBook")

        self.BookName = QtWidgets.QLabel(Form)
        self.BookName.setGeometry(QtCore.QRect(300, 280, 141, 21))
        self.BookName.setObjectName("BookName")

        self.AutorName = QtWidgets.QLabel(Form)
        self.AutorName.setGeometry(QtCore.QRect(300, 330, 141, 21))
        self.AutorName.setObjectName("AutorName")

        self.CoverBookLabel = QLabel(Form)
        self.CoverBookLabel.setGeometry(QtCore.QRect(83, 160, 180, 270))
        self.CoverBookLabel.setObjectName("CoverBookLabel")

        self.AddCoverButton = QtWidgets.QPushButton(Form)
        self.AddCoverButton.setGeometry(QtCore.QRect(83, 160, 180, 270))
        self.AddCoverButton.setObjectName("AddCoverButton")

        self.BookNameEdit = QtWidgets.QLineEdit(Form)
        self.BookNameEdit.setGeometry(QtCore.QRect(450, 270, 291, 41))
        self.BookNameEdit.setObjectName("BookNameEdit")

        self.AutorNameEdit = QtWidgets.QLineEdit(Form)
        self.AutorNameEdit.setGeometry(QtCore.QRect(450, 320, 291, 41))
        self.AutorNameEdit.setObjectName("AutorNameEdit")

        self.ErrorText = QtWidgets.QLabel(Form)
        self.ErrorText.setGeometry(QtCore.QRect(460, 220, 281, 41))
        self.ErrorText.setText("")
        self.ErrorText.setObjectName("ErrorText")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 440, 91, 16))
        self.label.setObjectName("label")

        self.BackToMainButton = QtWidgets.QPushButton(Form)
        self.BackToMainButton.setGeometry(QtCore.QRect(10, 566, 91, 30))
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
