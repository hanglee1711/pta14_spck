import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QInputDialog,
    QMessageBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor

from main import Ui_MainWindow

DATA_FILE = "tasks.json"


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối nút
        self.ui.btnAddTask.clicked.connect(self.add_task)
        self.ui.btnDelete.clicked.connect(self.delete_task)
        self.ui.btnDone.clicked.connect(self.mark_done)

        self.notified_tasks = set()

        # Load task
        self.load_tasks()
        self.sort_tasks()
        self.update_colors()

        # Timer kiểm tra giờ
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time)
        self.timer.start(30000)  # 30 giây

    # =====================
    # LOAD TASK
    # =====================
    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.ui.listTask.clear()

        for task in data.get("tasks", []):
            text = f"⏰ {task['time']} | {task['text']}"
            if task.get("done"):
                text = "✔ " + text
            self.ui.listTask.addItem(text)

    # =====================
    # SAVE TASK
    # =====================
    def save_tasks(self):
        tasks = []

        for i in range(self.ui.listTask.count()):
            item = self.ui.listTask.item(i)
            text = item.text()
            done = text.startswith("✔")

            clean = text.replace("✔ ", "")
            time_part, task_text = clean.split(" | ", 1)

            tasks.append({
                "text": task_text,
                "time": time_part.replace("⏰ ", ""),
                "done": done
            })

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=4)

    # =====================
    # ADD TASK
    # =====================
    def add_task(self):
        task, ok = QInputDialog.getText(self, "Thêm công việc", "Tên công việc:")
        if not ok or not task.strip():
            return

        time_str, ok = QInputDialog.getText(
            self,
            "Hẹn giờ",
            "Nhập ngày giờ (YYYY-MM-DD HH:MM)"
        )
        if not ok:
            return

        try:
            dt = datetime.strptime(time_str.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Sai định dạng ngày giờ!")
            return

        display = f"⏰ {dt.strftime('%Y-%m-%d %H:%M')} | {task.strip()}"
        self.ui.listTask.addItem(display)
        self.save_tasks()
        self.update_colors()
        self.sort_tasks()

    # =====================
    # DELETE TASK
    # =====================
    def delete_task(self):
        item = self.ui.listTask.currentItem()
        if not item:
            QMessageBox.warning(self, "Lỗi", "Chọn công việc cần xóa!")
            return

        self.ui.listTask.takeItem(self.ui.listTask.row(item))
        self.save_tasks()

    # =====================
    # MARK DONE
    # =====================
    def mark_done(self):
        item = self.ui.listTask.currentItem()
        if not item:
            QMessageBox.warning(self, "Lỗi", "Chọn công việc!")
            return

        if not item.text().startswith("✔"):
            item.setText("✔ " + item.text())
            item.setForeground(QColor("lightgreen"))
            self.save_tasks()
            self.sort_tasks()

    # =====================
    # CHECK TIME (NHẮC + ĐỔI MÀU)
    # =====================
    def check_time(self):
        now = datetime.now()

        for i in range(self.ui.listTask.count()):
            item = self.ui.listTask.item(i)
            text = item.text()

            if text.startswith("✔"):
                continue

            clean = text.replace("✔ ", "")
            time_part, _ = clean.split(" | ", 1)
            task_time = datetime.strptime(
                time_part.replace("⏰ ", ""),
                "%Y-%m-%d %H:%M"
            )

            diff = (task_time - now).total_seconds() / 60

            # 🔔 NHẮC ĐÚNG GIỜ
            if -0.5 <= diff <= 0.5 and text not in self.notified_tasks:
                QMessageBox.information(
                    self,
                    "⏰ Nhắc việc",
                    f"Đến giờ: {clean}"
                )
                self.notified_tasks.add(text)

        self.update_colors()
        self.sort_tasks()

    # =====================
    # UPDATE MÀU TASK
    # =====================
    def update_colors(self):
        now = datetime.now()

        for i in range(self.ui.listTask.count()):
            item = self.ui.listTask.item(i)
            text = item.text()

            if text.startswith("✔"):
                item.setForeground(QColor("lightgreen"))
                continue

            clean = text.replace("✔ ", "")
            time_part, _ = clean.split(" | ", 1)
            task_time = datetime.strptime(
                time_part.replace("⏰ ", ""),
                "%Y-%m-%d %H:%M"
            )

            diff = (task_time - now).total_seconds() / 60

            if diff < 0:
                item.setForeground(QColor("red"))       # 🔴 quá hạn
            elif diff <= 10:
                item.setForeground(QColor("orange"))    # 🟠 sắp tới
            else:
                item.setForeground(QColor("white"))     # ⚪ còn xa

    # =====================
    # SẮP XẾP TASK (quá hạn → gần → xa → done)
    # =====================
    def sort_tasks(self):
        now = datetime.now()
        task_items = []

        for i in range(self.ui.listTask.count()):
            item = self.ui.listTask.item(i)
            text = item.text()

            done = text.startswith("✔")
            clean = text.replace("✔ ", "")
            time_part, _ = clean.split(" | ", 1)

            task_time = datetime.strptime(time_part.replace("⏰ ", ""), "%Y-%m-%d %H:%M")
            diff = (task_time - now).total_seconds()

            if done:
                diff = float("inf")  # task done xuống cuối

            task_items.append((diff, text))

        # sort theo diff tăng dần
        task_items.sort(key=lambda x: x[0])

        # cập nhật lại list
        self.ui.listTask.clear()
        for _, text in task_items:
            self.ui.listTask.addItem(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())
