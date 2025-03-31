from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 851, 531))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgb(200, 200, 200);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.scrollArea.setObjectName("scrollArea")

        self.quotesContainer = QtWidgets.QWidget()
        self.quotesContainer.setStyleSheet("background: transparent;")
        self.quotesContainer.setObjectName("quotesContainer")
        self.quotesLayout = QtWidgets.QVBoxLayout(self.quotesContainer)
        self.quotesLayout.setSpacing(15)
        self.quotesLayout.setContentsMargins(10, 10, 10, 10)
        self.quotesLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea.setWidget(self.quotesContainer)

        self.AddQuoteButton = QtWidgets.QPushButton(Form)
        self.AddQuoteButton.setGeometry(QtCore.QRect(740, 570, 131, 23))
        self.AddQuoteButton.setStyleSheet("""
            QPushButton {
                background: rgb(255, 255, 255);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgb(240, 240, 240);
            }
        """)
        self.AddQuoteButton.setObjectName("AddQuoteButton")

        self.ReadyButtonAddText = QtWidgets.QPushButton(Form)
        self.ReadyButtonAddText.setGeometry(QtCore.QRect(20, 570, 101, 23))
        self.ReadyButtonAddText.setStyleSheet("""
            QPushButton {
                background: rgb(255, 255, 255);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgb(240, 240, 240);
            }
        """)
        self.ReadyButtonAddText.setObjectName("ReadyButtonAddText")

        self.DeletedQuote = QtWidgets.QPushButton(Form)
        self.DeletedQuote.setGeometry(QtCore.QRect(600, 570, 131, 23))
        self.DeletedQuote.setStyleSheet("""
            QPushButton {
                background: rgb(255, 255, 255);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgb(240, 240, 240);
            }
        """)
        self.DeletedQuote.setObjectName("DeletedQuote")

        self.DeletedBook = QtWidgets.QPushButton(Form)
        self.DeletedBook.setGeometry(QtCore.QRect(130, 570, 101, 23))
        self.DeletedBook.setStyleSheet("""
            QPushButton {
                background: rgb(255, 255, 255);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgb(240, 240, 240);
            }
        """)
        self.DeletedBook.setObjectName("DeletedBook")

        self.EditBookButton = QtWidgets.QPushButton(Form)
        self.EditBookButton.setGeometry(QtCore.QRect(240, 570, 101, 23))
        self.EditBookButton.setStyleSheet("""
            QPushButton {
                background: rgb(255, 255, 255);
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgb(240, 240, 240);
            }
        """)
        self.EditBookButton.setObjectName("EditBookButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавление цитаты"))
        self.AddQuoteButton.setText(_translate("Form", "Добавить цитату"))
        self.ReadyButtonAddText.setText(_translate("Form", "Готово"))
        self.DeletedQuote.setText(_translate("Form", "Удалить цитату"))
        self.DeletedBook.setText(_translate("Form", "Удалить книгу"))
        self.EditBookButton.setText(_translate("Form", "Изменить"))
