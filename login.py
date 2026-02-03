from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 500)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.card = QtWidgets.QFrame(parent=self.centralwidget)
        self.card.setGeometry(QtCore.QRect(210, 65, 300, 370))
        self.card.setObjectName("card")

        self.labelTitle = QtWidgets.QLabel(parent=self.card)
        self.labelTitle.setGeometry(QtCore.QRect(0, 20, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")

        self.lineEmail = QtWidgets.QLineEdit(parent=self.card)
        self.lineEmail.setGeometry(QtCore.QRect(35, 90, 230, 40))
        self.lineEmail.setObjectName("lineEmail")

        self.linePassword = QtWidgets.QLineEdit(parent=self.card)
        self.linePassword.setGeometry(QtCore.QRect(35, 150, 230, 40))
        self.linePassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.linePassword.setObjectName("linePassword")

        self.checkRemember = QtWidgets.QCheckBox(parent=self.card)
        self.checkRemember.setGeometry(QtCore.QRect(35, 205, 230, 20))
        self.checkRemember.setObjectName("checkRemember")

        self.btnLogin = QtWidgets.QPushButton(parent=self.card)
        self.btnLogin.setGeometry(QtCore.QRect(35, 240, 230, 40))
        self.btnLogin.setObjectName("btnLogin")

        self.label = QtWidgets.QLabel(parent=self.card)
        self.label.setGeometry(QtCore.QRect(35, 300, 230, 20))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login"))
        self.labelTitle.setText(_translate("MainWindow", "DANG NHAP"))
        self.lineEmail.setPlaceholderText(_translate("MainWindow", "Email"))
        self.linePassword.setPlaceholderText(_translate("MainWindow", "Password"))
        self.checkRemember.setText(_translate("MainWindow", "Remember me"))
        self.btnLogin.setText(_translate("MainWindow", "Login"))
        self.label.setText(_translate("MainWindow", "Create account"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
