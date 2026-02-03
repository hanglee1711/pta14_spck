import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*sipPyTypeDict.*")
import json
import os
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QColor, QFont, QCursor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QMessageBox,
    QGraphicsDropShadowEffect,
)
import login, register
import ghi_chu

USERS_FILE = "users.json"

GLOBAL_STYLESHEET = """
* {
    font-family: "Segoe UI";
}

QMainWindow, QWidget {
    background: #1a1a2e;
    color: #eaeaea;
}

QFrame#card {
    background: #16213e;
    border-radius: 20px;
    border: 1px solid #2a2a4a;
}

QLineEdit {
    background: #1a1a3e;
    color: #eaeaea;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
}
QLineEdit:focus {
    border: 1px solid #5dade2;
}
QLineEdit::placeholder {
    color: #a0a0b8;
}

QPushButton {
    background: #e94560;
    color: #eaeaea;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background: #d63851;
}

QCheckBox {
    color: #a0a0b8;
    font-size: 12px;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #2a2a4a;
    border-radius: 3px;
    background: #1a1a3e;
}
QCheckBox::indicator:checked {
    background: #5dade2;
    border-color: #5dade2;
}

QLabel {
    color: #eaeaea;
    background: transparent;
}

QLabel#label, QLabel#labelLogin {
    color: #5dade2;
    font-size: 11px;
    font-weight: bold;
}

QListWidget {
    background: #16213e;
    color: #eaeaea;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 4px;
    font-size: 13px;
    outline: none;
}
QListWidget::item {
    padding: 8px 10px;
    border-radius: 6px;
}
QListWidget::item:selected {
    background: #0f3460;
    color: #eaeaea;
}
QListWidget::item:hover {
    background: #1a1a3e;
}

QTextEdit {
    background: #16213e;
    color: #eaeaea;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px;
    font-size: 13px;
}
QTextEdit:focus {
    border: 1px solid #5dade2;
}

QScrollBar:vertical {
    background: #1a1a2e;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #2a2a4a;
    min-height: 30px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #5dade2;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #1a1a2e;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background: #2a2a4a;
    min-width: 30px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #5dade2;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

QMessageBox {
    background: #16213e;
    color: #eaeaea;
}
QMessageBox QLabel {
    color: #eaeaea;
}
QMessageBox QPushButton {
    min-width: 80px;
}
"""


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def add_card_shadow(card_widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(30)
    shadow.setOffset(0, 8)
    shadow.setColor(QColor(0, 0, 0, 120))
    card_widget.setGraphicsEffect(shadow)


class LinkHoverFilter:
    """Event filter to add hover color change on link labels."""
    def __init__(self, label, normal_color="#5dade2", hover_color="#eaeaea"):
        self._label = label
        self._normal = normal_color
        self._hover = hover_color

    def eventFilter(self, obj, event):
        if obj is self._label:
            if event.type() == QEvent.Type.Enter:
                self._label.setStyleSheet(f"color: {self._hover}; font-weight: bold; background: transparent;")
                return True
            elif event.type() == QEvent.Type.Leave:
                self._label.setStyleSheet(f"color: {self._normal}; font-weight: bold; background: transparent;")
                return True
        return False


class LoginPage(QMainWindow):
    def __init__(self, stack):
        super().__init__()
        self.ui = login.Ui_MainWindow()
        self.ui.setupUi(self)
        self.stack = stack

        # Card drop shadow
        add_card_shadow(self.ui.card)

        # Link label: cursor + hover effect
        self.ui.label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._link_filter = LinkHoverFilter(self.ui.label)
        self.ui.label.installEventFilter(self)
        self.ui.label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        # Click "Create account"
        self.ui.label.mousePressEvent = self.goRegister

        # Click "Login"
        self.ui.btnLogin.clicked.connect(self.handle_login)

    def eventFilter(self, obj, event):
        if obj is self.ui.label:
            return self._link_filter.eventFilter(obj, event)
        return super().eventFilter(obj, event)

    def goRegister(self, event):
        self.stack.setCurrentIndex(1)

    def handle_login(self):
        email = self.ui.lineEmail.text().strip()
        password = self.ui.linePassword.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Loi", "Vui long nhap day du email va mat khau!")
            return

        users = load_users()
        for user in users:
            if user["email"] == email and user["password"] == password:
                self.stack.setCurrentIndex(2)
                return

        QMessageBox.warning(self, "Loi", "Email hoac mat khau khong dung!")


class RegisterPage(QMainWindow):
    def __init__(self, stack):
        super().__init__()
        self.ui = register.Ui_MainWindow()
        self.ui.setupUi(self)
        self.stack = stack

        # Card drop shadow
        add_card_shadow(self.ui.card)

        # Link label: cursor + hover effect
        self.ui.labelLogin.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._link_filter = LinkHoverFilter(self.ui.labelLogin)
        self.ui.labelLogin.installEventFilter(self)
        self.ui.labelLogin.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        # Click "Already have account? Login"
        self.ui.labelLogin.mousePressEvent = self.goLogin

        # Click "Register"
        self.ui.btnRegister.clicked.connect(self.handle_register)

    def eventFilter(self, obj, event):
        if obj is self.ui.labelLogin:
            return self._link_filter.eventFilter(obj, event)
        return super().eventFilter(obj, event)

    def goLogin(self, event):
        self.stack.setCurrentIndex(0)

    def handle_register(self):
        username = self.ui.lineUsername.text().strip()
        email = self.ui.lineEmail.text().strip()
        password = self.ui.linePassword.text().strip()
        confirm = self.ui.lineConfirm.text().strip()

        if not username or not email or not password or not confirm:
            QMessageBox.warning(self, "Loi", "Vui long nhap day du thong tin!")
            return

        if password != confirm:
            QMessageBox.warning(self, "Loi", "Mat khau xac nhan khong khop!")
            return

        if not self.ui.checkTerms.isChecked():
            QMessageBox.warning(self, "Loi", "Ban can dong y voi dieu khoan!")
            return

        users = load_users()
        for user in users:
            if user["email"] == email:
                QMessageBox.warning(self, "Loi", "Email da duoc dang ky!")
                return

        users.append({
            "username": username,
            "email": email,
            "password": password
        })
        save_users(users)

        QMessageBox.information(self, "Thanh cong", "Dang ky thanh cong! Hay dang nhap.")
        self.stack.setCurrentIndex(0)


app = QApplication(sys.argv)
app.setStyleSheet(GLOBAL_STYLESHEET)
app.setFont(QFont("Segoe UI", 10))

stack = QStackedWidget()

login_page = LoginPage(stack)
register_page = RegisterPage(stack)
note_page = ghi_chu.NoteApp(stack=stack)

stack.addWidget(login_page)      # index 0
stack.addWidget(register_page)   # index 1
stack.addWidget(note_page)       # index 2

main_window = QMainWindow()
main_window.setWindowTitle("XNote")
main_window.setCentralWidget(stack)
main_window.setFixedSize(720, 500)
main_window.show()

sys.exit(app.exec())
