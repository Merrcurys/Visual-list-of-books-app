from PyQt6 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 847, 531))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.quotesContainer = QtWidgets.QWidget()
        self.quotesContainer.setObjectName("quotesContainer")
        self.quotesLayout = QtWidgets.QVBoxLayout(self.quotesContainer)
        self.quotesLayout.setSpacing(15)
        self.quotesLayout.setContentsMargins(10, 10, 10, 10)
        self.quotesLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scrollArea.setWidget(self.quotesContainer)

        self.ReadyButtonAddText = QtWidgets.QPushButton(Form)
        self.ReadyButtonAddText.setGeometry(QtCore.QRect(20, 566, 101, 30))
        self.ReadyButtonAddText.setObjectName("ReadyButtonAddText")

        self.DeletedQuote = QtWidgets.QPushButton(Form)
        self.DeletedQuote.setGeometry(QtCore.QRect(606, 566, 121, 30))
        self.DeletedQuote.setObjectName("DeletedQuote")

        self.AddQuoteButton = QtWidgets.QPushButton(Form)
        self.AddQuoteButton.setGeometry(QtCore.QRect(736, 566, 141, 30))
        self.AddQuoteButton.setObjectName("AddQuoteButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Цитаты книги"))
        self.AddQuoteButton.setText(_translate("Form", "Добавить цитату"))
        self.ReadyButtonAddText.setText(_translate("Form", "Готово"))
        self.DeletedQuote.setText(_translate("Form", "Удалить цитату"))
