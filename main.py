import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QCheckBox, QFrame, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPainterPath, QIcon

from database import Database
from dashboard import DashboardWidget


# ════════════════════════════════════════════════════════════
#  Shared styles
# ════════════════════════════════════════════════════════════
AUTH_STYLE = """
QWidget#authPage {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #EFF6FF, stop:1 #F0F7FF);
}
#authCard {
    background: white;
    border-radius: 20px;
    border: 1px solid #E2E8F0;
}
#authTitle {
    font-size: 28px;
    font-weight: bold;
    color: #1E293B;
}
#authSubtitle {
    font-size: 14px;
    color: #64748B;
}
#fieldLabel {
    font-size: 13px;
    font-weight: 600;
    color: #475569;
}
#authInput {
    padding: 12px 16px;
    border: 2px solid #E2E8F0;
    border-radius: 12px;
    font-size: 14px;
    background: #F8FAFC;
    color: #1E293B;
}
#authInput:focus {
    border-color: #3B82F6;
    background: white;
}
#primaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3B82F6, stop:1 #6366F1);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px;
    font-size: 16px;
    font-weight: 600;
}
#primaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2563EB, stop:1 #4F46E5);
}
#primaryBtn:pressed {
    background: #1D4ED8;
}
#linkBtn {
    background: none;
    border: none;
    color: #3B82F6;
    font-size: 13px;
    font-weight: 500;
    text-decoration: underline;
}
#linkBtn:hover {
    color: #2563EB;
}
#checkBox {
    font-size: 13px;
    color: #64748B;
}
#decorPanel {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #3B82F6, stop:0.5 #6366F1, stop:1 #8B5CF6);
    border-radius: 20px;
}
#decorTitle {
    color: white;
    font-size: 26px;
    font-weight: bold;
}
#decorText {
    color: rgba(255,255,255,200);
    font-size: 14px;
}
#errorLabel {
    color: #EF4444;
    font-size: 12px;
    font-weight: 500;
}
"""


def _decor_panel(title, subtitle):
    """Create the decorative right panel for auth pages."""
    panel = QFrame()
    panel.setObjectName("decorPanel")
    panel.setMinimumWidth(380)

    lay = QVBoxLayout(panel)
    lay.setContentsMargins(40, 60, 40, 60)
    lay.setSpacing(14)
    lay.addStretch()

    # Draw a simple school icon
    icon_label = QLabel()
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    px = QPixmap(120, 120)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(255, 255, 255, 60))
    p.drawEllipse(10, 10, 100, 100)
    # Book shape
    p.setBrush(QColor(255, 255, 255, 200))
    book = QPainterPath()
    book.moveTo(60, 28)
    book.lineTo(30, 35)
    book.lineTo(30, 85)
    book.lineTo(60, 78)
    book.lineTo(90, 85)
    book.lineTo(90, 35)
    book.closeSubpath()
    p.drawPath(book)
    # Center line
    from PyQt6.QtGui import QPen
    p.setPen(QPen(QColor("#6366F1"), 2))
    p.drawLine(60, 28, 60, 78)
    p.end()
    icon_label.setPixmap(px)
    lay.addWidget(icon_label)

    lay.addSpacing(10)

    t = QLabel(title)
    t.setObjectName("decorTitle")
    t.setAlignment(Qt.AlignmentFlag.AlignCenter)
    t.setWordWrap(True)
    lay.addWidget(t)

    s = QLabel(subtitle)
    s.setObjectName("decorText")
    s.setAlignment(Qt.AlignmentFlag.AlignCenter)
    s.setWordWrap(True)
    lay.addWidget(s)

    lay.addStretch()
    return panel


# ════════════════════════════════════════════════════════════
#  Login Page
# ════════════════════════════════════════════════════════════
class LoginPage(QWidget):
    def __init__(self, db, on_login, on_goto_register, parent=None):
        super().__init__(parent)
        self.db = db
        self.on_login = on_login
        self.on_goto_register = on_goto_register
        self.setObjectName("authPage")
        self.setStyleSheet(AUTH_STYLE)
        self._build()

    def _build(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 40)
        root.setSpacing(30)

        # Left: form card
        card = QFrame()
        card.setObjectName("authCard")
        card.setMaximumWidth(460)
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        form = QVBoxLayout(card)
        form.setContentsMargins(40, 40, 40, 40)
        form.setSpacing(10)

        title = QLabel("Chào mừng trở lại!")
        title.setObjectName("authTitle")
        form.addWidget(title)

        sub = QLabel("Đăng nhập vào tài khoản học sinh của bạn")
        sub.setObjectName("authSubtitle")
        form.addWidget(sub)
        form.addSpacing(16)

        form.addWidget(self._label("Email"))
        self.email = QLineEdit()
        self.email.setObjectName("authInput")
        self.email.setPlaceholderText("Nhập địa chỉ email...")
        self.email.setMinimumHeight(46)
        form.addWidget(self.email)
        form.addSpacing(6)

        form.addWidget(self._label("Mật khẩu"))
        self.password = QLineEdit()
        self.password.setObjectName("authInput")
        self.password.setPlaceholderText("Nhập mật khẩu...")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setMinimumHeight(46)
        form.addWidget(self.password)

        self.error = QLabel("")
        self.error.setObjectName("errorLabel")
        form.addWidget(self.error)

        self.remember = QCheckBox("Ghi nhớ đăng nhập")
        self.remember.setObjectName("checkBox")
        form.addWidget(self.remember)
        form.addSpacing(8)

        btn = QPushButton("ĐĂNG NHẬP")
        btn.setObjectName("primaryBtn")
        btn.setMinimumHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._login)
        form.addWidget(btn)

        form.addSpacing(10)
        row = QHBoxLayout()
        row.addStretch()
        link = QPushButton("Chưa có tài khoản? Đăng ký")
        link.setObjectName("linkBtn")
        link.setCursor(Qt.CursorShape.PointingHandCursor)
        link.clicked.connect(self.on_goto_register)
        row.addWidget(link)
        row.addStretch()
        form.addLayout(row)
        form.addStretch()

        root.addWidget(card)

        # Right: decoration
        root.addWidget(
            _decor_panel(
                "Quản lý học tập\nthông minh",
                "Theo dõi kết quả, lịch học\nvà thông báo dễ dàng"
            ),
            1
        )

        # Enter key triggers login
        self.password.returnPressed.connect(self._login)
        self.email.returnPressed.connect(lambda: self.password.setFocus())

    def _label(self, text):
        l = QLabel(text)
        l.setObjectName("fieldLabel")
        return l

    def _login(self):
        email = self.email.text().strip()
        pwd = self.password.text().strip()
        if not email or not pwd:
            self.error.setText("Vui lòng nhập đầy đủ email và mật khẩu")
            return
        result = self.db.authenticate(email, pwd)
        if result:
            self.error.setText("")
            self.on_login(result[0], result[1])
        else:
            self.error.setText("Email hoặc mật khẩu không đúng")


# ════════════════════════════════════════════════════════════
#  Register Page
# ════════════════════════════════════════════════════════════
class RegisterPage(QWidget):
    def __init__(self, db, on_registered, on_goto_login, parent=None):
        super().__init__(parent)
        self.db = db
        self.on_registered = on_registered
        self.on_goto_login = on_goto_login
        self.setObjectName("authPage")
        self.setStyleSheet(AUTH_STYLE)
        self._build()

    def _build(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 40)
        root.setSpacing(30)

        # Left: decoration
        root.addWidget(
            _decor_panel(
                "Bắt đầu hành trình\nhọc tập",
                "Tạo tài khoản để truy cập\nđầy đủ tính năng"
            ),
            1
        )

        # Right: form card
        card = QFrame()
        card.setObjectName("authCard")
        card.setMaximumWidth(460)
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        form = QVBoxLayout(card)
        form.setContentsMargins(40, 40, 40, 40)
        form.setSpacing(10)

        title = QLabel("Tạo tài khoản mới")
        title.setObjectName("authTitle")
        form.addWidget(title)

        sub = QLabel("Điền thông tin bên dưới để đăng ký")
        sub.setObjectName("authSubtitle")
        form.addWidget(sub)
        form.addSpacing(12)

        form.addWidget(self._label("Họ và tên"))
        self.fullname = QLineEdit()
        self.fullname.setObjectName("authInput")
        self.fullname.setPlaceholderText("Nhập họ và tên...")
        self.fullname.setMinimumHeight(46)
        form.addWidget(self.fullname)
        form.addSpacing(4)

        form.addWidget(self._label("Email"))
        self.email = QLineEdit()
        self.email.setObjectName("authInput")
        self.email.setPlaceholderText("Nhập địa chỉ email...")
        self.email.setMinimumHeight(46)
        form.addWidget(self.email)
        form.addSpacing(4)

        form.addWidget(self._label("Mật khẩu"))
        self.password = QLineEdit()
        self.password.setObjectName("authInput")
        self.password.setPlaceholderText("Nhập mật khẩu...")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setMinimumHeight(46)
        form.addWidget(self.password)

        self.error = QLabel("")
        self.error.setObjectName("errorLabel")
        form.addWidget(self.error)

        self.agree = QCheckBox("Tôi đồng ý với điều khoản sử dụng")
        self.agree.setObjectName("checkBox")
        form.addWidget(self.agree)
        form.addSpacing(8)

        btn = QPushButton("ĐĂNG KÝ")
        btn.setObjectName("primaryBtn")
        btn.setMinimumHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._register)
        form.addWidget(btn)

        form.addSpacing(10)
        row = QHBoxLayout()
        row.addStretch()
        link = QPushButton("Đã có tài khoản? Đăng nhập")
        link.setObjectName("linkBtn")
        link.setCursor(Qt.CursorShape.PointingHandCursor)
        link.clicked.connect(self.on_goto_login)
        row.addWidget(link)
        row.addStretch()
        form.addLayout(row)
        form.addStretch()

        root.addWidget(card)

        self.password.returnPressed.connect(self._register)

    def _label(self, text):
        l = QLabel(text)
        l.setObjectName("fieldLabel")
        return l

    def _register(self):
        name = self.fullname.text().strip()
        email = self.email.text().strip()
        pwd = self.password.text().strip()

        if not name or not email or not pwd:
            self.error.setText("Vui lòng điền đầy đủ thông tin")
            return
        if not self.agree.isChecked():
            self.error.setText("Bạn cần đồng ý với điều khoản sử dụng")
            return
        if len(pwd) < 4:
            self.error.setText("Mật khẩu phải có ít nhất 4 ký tự")
            return

        uid = self.db.register_user(name, email, pwd)
        if uid:
            self.error.setText("")
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
            self.on_registered()
        else:
            self.error.setText("Email đã được sử dụng")


# ════════════════════════════════════════════════════════════
#  Main Window
# ════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý Học tập")
        self.resize(1280, 820)
        self.setMinimumSize(1000, 650)

        self.db = Database()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.login_page = LoginPage(
            self.db, self._on_login, self._show_register
        )
        self.register_page = RegisterPage(
            self.db, self._show_login, self._show_login
        )
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)

        self.dashboard = None

    def _show_login(self):
        self.stack.setCurrentWidget(self.login_page)

    def _show_register(self):
        self.stack.setCurrentWidget(self.register_page)

    def _on_login(self, user_id, fullname):
        if self.dashboard:
            self.stack.removeWidget(self.dashboard)
            self.dashboard.deleteLater()

        self.dashboard = DashboardWidget(self.db, user_id)
        self.dashboard.logout_requested.connect(self._logout)
        self.stack.addWidget(self.dashboard)
        self.stack.setCurrentWidget(self.dashboard)
        self.setWindowTitle(f"Quản lý Học tập - {fullname}")

    def _logout(self):
        if self.dashboard:
            self.stack.removeWidget(self.dashboard)
            self.dashboard.deleteLater()
            self.dashboard = None
        self.stack.setCurrentWidget(self.login_page)
        self.setWindowTitle("Quản lý Học tập")

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)


# ════════════════════════════════════════════════════════════
#  Entry point
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
