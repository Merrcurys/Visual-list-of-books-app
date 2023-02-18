from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")
        self.AddQuoteButton = QtWidgets.QPushButton(Form)
        self.AddQuoteButton.setGeometry(QtCore.QRect(770, 570, 101, 23))
        self.AddQuoteButton.setStyleSheet("background: rgb(255, 255, 255); border-radius: 5px;")
        self.AddQuoteButton.setObjectName("AddQuoteButton")
        self.ReadyButtonAddText = QtWidgets.QPushButton(Form)
        self.ReadyButtonAddText.setGeometry(QtCore.QRect(20, 570, 101, 23))
        self.ReadyButtonAddText.setStyleSheet("background: rgb(255, 255, 255); border-radius: 5px;")
        self.ReadyButtonAddText.setObjectName("ReadyButtonAddText")
        self.ListWidget = QtWidgets.QListWidget(Form)
        self.ListWidget.setGeometry(QtCore.QRect(20, 20, 851, 531))
        self.ListWidget.setStyleSheet(" font-size:22px")
        self.ListWidget.setObjectName("ListWidget")
        self.DeletedQuote = QtWidgets.QPushButton(Form)
        self.DeletedQuote.setGeometry(QtCore.QRect(660, 570, 101, 23))
        self.DeletedQuote.setStyleSheet("background: rgb(255, 255, 255); border-radius: 5px;")
        self.DeletedQuote.setObjectName("DeletedQuote")
        self.DeletedBook = QtWidgets.QPushButton(Form)
        self.DeletedBook.setGeometry(QtCore.QRect(130, 570, 101, 23))
        self.DeletedBook.setStyleSheet("background: rgb(255, 255, 255); border-radius: 5px;")
        self.DeletedBook.setObjectName("DeletedBook")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавление цитаты"))
        self.AddQuoteButton.setText(_translate("Form", "Добавить цитату"))
        self.ReadyButtonAddText.setText(_translate("Form", "Готово"))
        self.DeletedQuote.setText(_translate("Form", "Удалить цитату"))
        self.DeletedBook.setText(_translate("Form", "Удалить книгу"))
