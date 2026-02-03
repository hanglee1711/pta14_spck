import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget, QMessageBox
from PyQt6.QtCore import Qt
import login   # file login.py
import register  # file register.py
from cuoikhoa_lời_nhắc_app import DailyTodo  # file cuối cùng


# ====== Hàm kiểm tra email chung ======
def validateEmail(email: str) -> tuple[bool, str]:
    """
    Trả về (True, "") nếu email hợp lệ,
    Trả về (False, "thông báo lỗi") nếu email không hợp lệ
    """
    email = email.strip()
    if not email:
        return False, "Email không được để trống!"
    if "@" not in email or email.count("@") != 1 or email.startswith("@") or email.endswith("@"):
        return False, "Email không hợp lệ. Ví dụ: example@gmail.com"
    return True, ""


# ====== Login Page ======
class LoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.ui = login.Ui_MainWindow()
        self.ui.setupUi(self)
        self.stack = stack

        # Click "Create account"
        self.ui.labelCreate.mousePressEvent = self.goRegister

        # Click Login button
        self.ui.btnLogin.clicked.connect(self.checkEmail)

    def goRegister(self, event):
        self.stack.setCurrentIndex(1)

    def checkEmail(self):
        email = self.ui.lineEmail.text()
        valid, msg = validateEmail(email)
        if not valid:
            QMessageBox.warning(self, "Lỗi Email", msg)
            return

        # Email hợp lệ → mở màn hình cuối
        self.openFinalApp()

    def openFinalApp(self):
        self.final_window = DailyTodo(on_logout=self.handleLogout)
        self.final_window.show()
        self.stack.hide()

    def handleLogout(self):
        self.ui.lineEmail.clear()
        self.ui.linePassword.clear()
        self.stack.setCurrentIndex(0)
        self.stack.show()


# ====== Register Page ======
class RegisterPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.ui = register.Ui_MainWindow()
        self.ui.setupUi(self)
        self.stack = stack

        # Click "Already have account? Login"
        self.ui.labelLogin.mousePressEvent = self.goLogin

        # Click Register button
        self.ui.btnRegister.clicked.connect(self.checkEmail)

    def goLogin(self, event):
        self.stack.setCurrentIndex(0)

    def checkEmail(self):
        email = self.ui.lineEmail.text()
        valid, msg = validateEmail(email)
        if not valid:
            QMessageBox.warning(self, "Lỗi Email", msg)
            return

        # Email hợp lệ → mở màn hình cuối
        self.openFinalApp()

    def openFinalApp(self):
        self.final_window = DailyTodo(on_logout=self.handleLogout)
        self.final_window.show()
        self.stack.hide()

    def handleLogout(self):
        self.ui.lineEmail.clear()
        self.stack.setCurrentIndex(0)
        self.stack.show()


# ====== Main ======
if __name__ == "__main__":
    app = QApplication(sys.argv)

    stack = QStackedWidget()
    stack.setFixedSize(720, 500)
    stack.setWindowTitle("LỜI NHẮC")

    # Apply gradient directly to QStackedWidget
    stack.setStyleSheet("""
        QStackedWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #11998e,
                stop:1 #38ef7d);
        }
    """)

    login_page = LoginPage(stack)
    register_page = RegisterPage(stack)

    stack.addWidget(login_page)      # index 0
    stack.addWidget(register_page)   # index 1

    stack.show()

    sys.exit(app.exec())
