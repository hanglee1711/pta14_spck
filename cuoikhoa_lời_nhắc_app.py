import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QListWidget, QMessageBox,
    QListWidgetItem, QComboBox, QLabel
)
from PyQt6.QtGui import QFont, QColor, QBrush, QCursor
from PyQt6.QtCore import Qt

FILE_PATH = "tasks.txt"


class DailyTodo(QWidget):
    def __init__(self, on_logout=None):
        super().__init__()
        self._on_logout = on_logout

        # ===== CỬA SỔ =====
        self.setWindowTitle("Daily Todo - PTA Easy")
        self.setGeometry(300, 100, 700, 600)
        self.setMinimumSize(650, 580)

        # ===== STYLE =====
        self.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: white;
            font-family: Arial;
        }
        QLineEdit {
            background-color: #1e1e1e;
            border: 2px solid #2a4a3f;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 2px solid #11998e;
        }
        QComboBox {
            background-color: #1e1e1e;
            border: 2px solid #2a4a3f;
            border-radius: 10px;
            padding: 8px;
        }
        QComboBox:focus {
            border: 2px solid #11998e;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #11998e;
            margin-right: 10px;
        }
        QComboBox QAbstractItemView {
            background-color: #1e1e1e;
            color: white;
            selection-background-color: #1a3a2f;
            selection-color: #38ef7d;
            border: 1px solid #2a4a3f;
            border-radius: 6px;
            padding: 4px;
        }
        QPushButton {
            border-radius: 12px;
            padding: 10px;
            font-size: 14px;
        }
        QListWidget {
            background-color: #1a1a1a;
            border: 2px solid #2a4a3f;
            border-radius: 10px;
            padding: 5px;
        }
        QListWidget:focus {
            border: 2px solid #11998e;
        }
        QListWidget::item {
            padding: 8px;
            margin: 4px;
            border-radius: 6px;
        }
        QListWidget::item:selected {
            background-color: #1a3a2f;
        }
        """)

        # ===== LAYOUT =====
        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # ===== INPUT =====
        self.input_task = QLineEdit()
        self.input_task.setPlaceholderText("Nhập công việc")
        self.input_task.setFont(QFont("Arial", 12))

        # ===== PRIORITY =====
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Cao", "Trung bình", "Thấp"])
        self.priority_combo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # ===== BUTTONS =====
        btn_cursor = QCursor(Qt.CursorShape.PointingHandCursor)

        self.add_button = QPushButton("➕ Thêm công việc")
        self.add_button.setStyleSheet("""
            QPushButton { background-color: #2196f3; }
            QPushButton:hover { background-color: #42a5f5; }
            QPushButton:pressed { background-color: #1976d2; }
        """)
        self.add_button.setCursor(btn_cursor)
        self.add_button.clicked.connect(self.add_task)

        self.complete_button = QPushButton("✅ Hoàn thành")
        self.complete_button.setStyleSheet("""
            QPushButton { background-color: #4caf50; }
            QPushButton:hover { background-color: #66bb6a; }
            QPushButton:pressed { background-color: #388e3c; }
        """)
        self.complete_button.setCursor(btn_cursor)
        self.complete_button.clicked.connect(self.complete_task)

        self.delete_button = QPushButton("🗑️ Xóa")
        self.delete_button.setStyleSheet("""
            QPushButton { background-color: #f44336; }
            QPushButton:hover { background-color: #ef5350; }
            QPushButton:pressed { background-color: #d32f2f; }
        """)
        self.delete_button.setCursor(btn_cursor)
        self.delete_button.clicked.connect(self.delete_task)

        self.incomplete_button = QPushButton("📌 Chưa hoàn thành")
        self.incomplete_button.setStyleSheet("""
            QPushButton { background-color: #ff9800; }
            QPushButton:hover { background-color: #ffa726; }
            QPushButton:pressed { background-color: #f57c00; }
        """)
        self.incomplete_button.setCursor(btn_cursor)
        self.incomplete_button.clicked.connect(self.show_incomplete)

        self.clear_all_button = QPushButton("🧹 Xóa tất cả")
        self.clear_all_button.setStyleSheet("""
            QPushButton { background-color: #9e9e9e; }
            QPushButton:hover { background-color: #bdbdbd; }
            QPushButton:pressed { background-color: #757575; }
        """)
        self.clear_all_button.setCursor(btn_cursor)
        self.clear_all_button.clicked.connect(self.clear_all)

        self.logout_button = QPushButton("🚪 Đăng xuất")
        self.logout_button.setStyleSheet("""
            QPushButton { background-color: #37474f; }
            QPushButton:hover { background-color: #546e7a; }
            QPushButton:pressed { background-color: #263238; }
        """)
        self.logout_button.setCursor(btn_cursor)
        self.logout_button.clicked.connect(self.logout)

        # ===== COUNTER =====
        self.done_label = QLabel("✅ Hoàn thành: 0")
        self.done_label.setFont(QFont("Arial", 11))
        self.done_label.setStyleSheet("""
            background-color: #1a3a2f;
            color: #38ef7d;
            border-radius: 8px;
            padding: 6px 10px;
        """)

        self.todo_label = QLabel("⏳ Chưa hoàn thành: 0")
        self.todo_label.setFont(QFont("Arial", 11))
        self.todo_label.setStyleSheet("""
            background-color: #3a2a1a;
            color: #ff9800;
            border-radius: 8px;
            padding: 6px 10px;
        """)

        # ===== LEFT =====
        left_layout.addWidget(self.input_task)
        left_layout.addWidget(self.priority_combo)
        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.complete_button)
        left_layout.addWidget(self.delete_button)
        left_layout.addWidget(self.incomplete_button)
        left_layout.addWidget(self.clear_all_button)
        left_layout.addWidget(self.logout_button)
        left_layout.addSpacing(15)
        left_layout.addWidget(self.done_label)
        left_layout.addWidget(self.todo_label)
        left_layout.addStretch()

        # ===== RIGHT =====
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Arial", 11))
        right_layout.addWidget(self.list_widget)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        self.load_tasks()

    # ===== STYLE ITEM =====
    def set_item_style(self, item, status, priority, text):
        if priority == "Cao":
            item.setText(f"⚡ {text}")
            item.setForeground(QBrush(QColor("red")))
        elif priority == "Trung bình":
            item.setText(f"⭐ {text}")
            item.setForeground(QBrush(QColor("orange")))
        else:
            item.setText(f"💤 {text}")
            item.setForeground(QBrush(QColor("deepskyblue")))

        if status == "[X]":
            item.setForeground(QBrush(QColor("lightgreen")))

    # ===== UPDATE COUNTER =====
    def update_counter(self):
        done = 0
        todo = 0
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("[X]"):
                        done += 1
                    elif line.startswith("[ ]"):
                        todo += 1
        except FileNotFoundError:
            pass

        self.done_label.setText(f"✅ Hoàn thành: {done}")
        self.todo_label.setText(f"⏳ Chưa hoàn thành: {todo}")

    # ===== LOAD =====
    def load_tasks(self):
        self.list_widget.clear()
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        status, priority, name = [p.strip() for p in parts]
                        item = QListWidgetItem()
                        self.set_item_style(item, status, priority, line.strip())
                        self.list_widget.addItem(item)
        except FileNotFoundError:
            open(FILE_PATH, "w", encoding="utf-8").close()

        self.update_counter()

    # ===== ADD =====
    def add_task(self):
        task = self.input_task.text().strip()
        priority = self.priority_combo.currentText()
        if not task:
            QMessageBox.warning(self, "Lỗi", "Bạn chưa nhập công việc!")
            return

        with open(FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[ ] | {priority} | {task}\n")

        self.input_task.clear()
        self.load_tasks()

    # ===== COMPLETE =====
    def complete_task(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        text = item.text()[2:]
        if text.startswith("[X]"):
            return

        parts = text.split("|")
        parts[0] = "[X]"
        updated = " | ".join(p.strip() for p in parts)

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            tasks = f.read().splitlines()

        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for t in tasks:
                f.write((updated if t.strip() == text.strip() else t) + "\n")

        self.load_tasks()

    # ===== DELETE =====
    def delete_task(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        text = item.text()[2:]

        with open(FILE_PATH, "r", encoding="utf-8") as f:
            tasks = f.read().splitlines()

        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for t in tasks:
                if t.strip() != text.strip():
                    f.write(t + "\n")

        self.load_tasks()

    # ===== SHOW INCOMPLETE =====
    def show_incomplete(self):
        self.list_widget.clear()
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("[ ]"):
                    parts = line.split("|")
                    priority = parts[1].strip()
                    item = QListWidgetItem()
                    self.set_item_style(item, "[ ]", priority, line.strip())
                    self.list_widget.addItem(item)

    # ===== LOGOUT =====
    def logout(self):
        if self._on_logout:
            self._on_logout()
        self.close()

    # ===== CLEAR ALL =====
    def clear_all(self):
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn xóa tất cả?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            open(FILE_PATH, "w", encoding="utf-8").close()
            self.list_widget.clear()
            self.update_counter()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DailyTodo()
    window.show()
    sys.exit(app.exec())
