from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(887, 611)
        Form.setStyleSheet("")

        self.SettingsName = QtWidgets.QLabel(Form)
        self.SettingsName.setGeometry(QtCore.QRect(390, 40, 101, 21))
        self.SettingsName.setStyleSheet("font-size: 18px; ")
        self.SettingsName.setObjectName("SettingsName")

        self.Import = QtWidgets.QPushButton(Form)
        self.Import.setGeometry(QtCore.QRect(520, 240, 271, 181))
        self.Import.setStyleSheet("background: rgb(255, 255, 255);")
        self.Import.setObjectName("Import")

        self.Export = QtWidgets.QPushButton(Form)
        self.Export.setGeometry(QtCore.QRect(100, 240, 271, 181))
        self.Export.setStyleSheet("background: rgb(255, 255, 255);")
        self.Export.setObjectName("Export")

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
        self.SettingsName.setText(_translate("Form", "НАСТРОЙКИ"))
        self.Import.setText(_translate("Form", "Импорт"))
        self.BackToMainButton.setText(_translate("Form", "Назад"))
        self.Export.setText(_translate("Form", "Экспорт"))
