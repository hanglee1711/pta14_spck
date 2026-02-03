from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 500)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.card = QtWidgets.QFrame(parent=self.centralwidget)
        self.card.setGeometry(QtCore.QRect(210, 20, 300, 460))
        self.card.setObjectName("card")

        self.labelTitle = QtWidgets.QLabel(parent=self.card)
        self.labelTitle.setGeometry(QtCore.QRect(0, 15, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        self.labelTitle.setFont(font)
        self.labelTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")

        self.lineUsername = QtWidgets.QLineEdit(parent=self.card)
        self.lineUsername.setGeometry(QtCore.QRect(35, 75, 230, 40))
        self.lineUsername.setObjectName("lineUsername")

        self.lineEmail = QtWidgets.QLineEdit(parent=self.card)
        self.lineEmail.setGeometry(QtCore.QRect(35, 135, 230, 40))
        self.lineEmail.setObjectName("lineEmail")

        self.linePassword = QtWidgets.QLineEdit(parent=self.card)
        self.linePassword.setGeometry(QtCore.QRect(35, 195, 230, 40))
        self.linePassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.linePassword.setObjectName("linePassword")

        self.lineConfirm = QtWidgets.QLineEdit(parent=self.card)
        self.lineConfirm.setGeometry(QtCore.QRect(35, 255, 230, 40))
        self.lineConfirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineConfirm.setObjectName("lineConfirm")

        self.checkTerms = QtWidgets.QCheckBox(parent=self.card)
        self.checkTerms.setGeometry(QtCore.QRect(35, 315, 230, 20))
        self.checkTerms.setObjectName("checkTerms")

        self.btnRegister = QtWidgets.QPushButton(parent=self.card)
        self.btnRegister.setGeometry(QtCore.QRect(35, 350, 230, 40))
        self.btnRegister.setObjectName("btnRegister")

        self.labelLogin = QtWidgets.QLabel(parent=self.card)
        self.labelLogin.setGeometry(QtCore.QRect(35, 410, 230, 20))
        self.labelLogin.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelLogin.setObjectName("labelLogin")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Register"))
        self.labelTitle.setText(_translate("MainWindow", "DANG KY"))
        self.lineUsername.setPlaceholderText(_translate("MainWindow", "Username"))
        self.lineEmail.setPlaceholderText(_translate("MainWindow", "Email"))
        self.linePassword.setPlaceholderText(_translate("MainWindow", "Password"))
        self.lineConfirm.setPlaceholderText(_translate("MainWindow", "Confirm Password"))
        self.checkTerms.setText(_translate("MainWindow", "I agree to the terms"))
        self.btnRegister.setText(_translate("MainWindow", "Register"))
        self.labelLogin.setText(_translate("MainWindow", "Already have an account? Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
