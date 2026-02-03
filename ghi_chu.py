import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget,
    QTextEdit, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QMessageBox
)

DATA_FILE = "notes.json"


class NoteApp(QMainWindow):
    def __init__(self, stack=None):
        super().__init__()
        self.setWindowTitle("XNote")
        self.setGeometry(300, 200, 700, 400)

        self.stack = stack
        self.notes = []
        self.current_index = None

        self.init_ui()
        self.load_notes()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        # ===== LEFT PANEL =====
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setObjectName("btnLogout")
        self.btn_logout.clicked.connect(self.handle_logout)
        self.btn_logout.setStyleSheet("""
            QPushButton#btnLogout {
                background: transparent;
                color: #e94560;
                border: 1px solid #e94560;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton#btnLogout:hover {
                background: #e94560;
                color: #eaeaea;
            }
        """)

        self.list_notes = QListWidget()
        self.list_notes.clicked.connect(self.show_note)

        btn_add = QPushButton("+ Them")
        btn_add.setObjectName("btnAdd")
        btn_add.clicked.connect(self.add_note)
        btn_add.setStyleSheet("""
            QPushButton#btnAdd {
                background: transparent;
                color: #5dade2;
                border: 1px solid #5dade2;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton#btnAdd:hover {
                background: #5dade2;
                color: #1a1a2e;
            }
        """)

        btn_delete = QPushButton("Xoa")
        btn_delete.setObjectName("btnDelete")
        btn_delete.clicked.connect(self.delete_note)
        btn_delete.setStyleSheet("""
            QPushButton#btnDelete {
                background: transparent;
                color: #e94560;
                border: 1px solid #e94560;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton#btnDelete:hover {
                background: #e94560;
                color: #eaeaea;
            }
        """)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        left_layout.addWidget(self.btn_logout)
        left_layout.addWidget(self.list_notes)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_delete)
        left_layout.addLayout(btn_row)

        # ===== RIGHT PANEL =====
        self.txt_title = QLineEdit()
        self.txt_title.setPlaceholderText("Tieu de ghi chu")

        self.txt_content = QTextEdit()
        self.txt_content.setPlaceholderText("Noi dung ghi chu...")

        btn_save = QPushButton("Luu")
        btn_save.setObjectName("btnSave")
        btn_save.clicked.connect(self.save_note)
        btn_save.setStyleSheet("""
            QPushButton#btnSave {
                background: #e94560;
                color: #eaeaea;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#btnSave:hover {
                background: #d63851;
            }
        """)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        right_layout.addWidget(self.txt_title)
        right_layout.addWidget(self.txt_content)
        right_layout.addWidget(btn_save)

        # ===== MAIN LAYOUT =====
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 5)

        central.setLayout(main_layout)

    def handle_logout(self):
        if self.stack:
            self.stack.setCurrentIndex(0)

    def load_notes(self):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.notes = json.load(f)
            for note in self.notes:
                self.list_notes.addItem(note["title"])
        except Exception:
            self.notes = []

    def save_notes_to_file(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=4)

    def add_note(self):
        self.txt_title.clear()
        self.txt_content.clear()
        self.current_index = None

    def save_note(self):
        title = self.txt_title.text().strip()
        content = self.txt_content.toPlainText()

        if not title:
            QMessageBox.warning(self, "Loi", "Chua nhap tieu de")
            return

        for i, note in enumerate(self.notes):
            if note["title"].lower() == title.lower():
                if self.current_index == i:
                    break
                QMessageBox.warning(
                    self,
                    "Canh bao",
                    "Tieu de ghi chu da ton tai!"
                )
                return

        if self.current_index is None:
            self.notes.append({
                "title": title,
                "content": content
            })
            self.list_notes.addItem(title)
        else:
            self.notes[self.current_index] = {
                "title": title,
                "content": content
            }
            self.list_notes.item(self.current_index).setText(title)

        self.save_notes_to_file()

    def show_note(self):
        self.current_index = self.list_notes.currentRow()
        note = self.notes[self.current_index]
        self.txt_title.setText(note["title"])
        self.txt_content.setText(note["content"])

    def delete_note(self):
        row = self.list_notes.currentRow()
        if row >= 0:
            self.list_notes.takeItem(row)
            self.notes.pop(row)
            self.save_notes_to_file()
            self.txt_title.clear()
            self.txt_content.clear()
            self.current_index = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec())
