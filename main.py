from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit,
    QSpacerItem, QSizePolicy, QWidgetItem, QMessageBox,
    QApplication, QMainWindow, QFrame
)
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation
from PyQt6.QtGui import QIcon
from data_manager import DataManager
import pyqtgraph as pg

import sys, time, requests, random, json, platform, pathlib

tld_site = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"

def path(s: str):
    if platform.system() == "Windows":
        return pathlib.PureWindowsPath(s)
    return s

with open(path("assets/lang/english.json"), "r") as ifs:
    raw_words = json.load(ifs)
WORDS: list[str] = raw_words["words"]

try:
    response = requests.get(tld_site, timeout=5)
    TLDS: list = response.content.decode('utf-8').splitlines()
    TLDS.pop(0)
except Exception:
    TLDS = ["COM", "NET", "ORG", "EDU", "GOV", "IO", "CO", "US", "UK", "VN", "INFO", "BIZ", "ME", "DEV", "APP"]

username: str = ""
password: str = ""

inactive_stylesheet = "color: rgb(192, 191, 188);background-color: rgba(255, 255, 255, 0);"
active_stylesheet = "color: rgb(255, 255, 255);background-color: rgba(255, 255, 255, 0);"
incorrect_stylesheet = "color: rgb(224, 27, 36);background-color: rgba(255, 255, 255, 0);"

CHARS_PER_LINE = 80

def generate_words():
    line = ""
    lines = []
    for i in range(1000):
        word = random.choice(WORDS)
        if (len(line) + len(word) + 1) > CHARS_PER_LINE:
            lines.append(line)
            line = ""
        line += word + " "
    return lines

def create_lines(parent: QWidget):
    first = True
    res: QLabel
    for i in range(3):
        line = QHBoxLayout()
        line.setSpacing(1)
        line.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        for j in range(CHARS_PER_LINE):
            item = QLabel(parent)
            item.setText(" ")
            font = QtGui.QFont()
            font.setPointSize(25)
            item.setFont(font)
            item.setStyleSheet(inactive_stylesheet)
            if first:
                first = False
                res = item

            line.addWidget(item)
        line.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        parent.lines.addLayout(line)

    parent.lines.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
    return res


def headedStr(s: str, level = 2) -> str:
    return f"<h{level}>{s}</h{level}>"

def showLogin(e = None):
    window.setCentralWidget(Login())

def showRegister(e = None):
    window.setCentralWidget(Register())

def login():
    if (not dman.login(username, password)):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Incorrect username or password")
        msg.exec()
        return
    MAIN = Main(username)
    window.setCentralWidget(MAIN)

class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(path("ui/login.ui"), self)
        self.login_button.clicked.connect(self.clicked)
        self.register_button.mousePressEvent = showRegister

    def clicked(self):
        global username, password
        username = self.username_box.text()
        password = self.password_box.text()
        login()

class Register(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(path("ui/register.ui"), self)
        self.reg_button.clicked.connect(self.registered)
        self.login_button.mousePressEvent = showLogin

    def registered(self):
        u = self.username_box_5.text()
        p = self.password_box.text()
        c_p = self.confirm_password_box.text()
        if len(p) < 6:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Password must be at least 6 characters")
            msg.exec()
            return
        if (p != c_p):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Passwords do not match")
            msg.exec()
            return
        email = self.email_box.text()
        if (not dman.register(u, email, p)):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Invalid username or email")
            msg.exec()
            return
        showLogin()

class Main(QWidget):
    def __init__(self, username: str):
        super().__init__()
        uic.loadUi(path("ui/lypa.ui"), self)

        self.text: QLabel
        self.lines: QVBoxLayout
        self.type: QLineEdit
        self.pointer: QFrame

        self.typed: str = ""

        self.username.setText(headedStr(username))

        self.logout_btn = QLabel(self)
        self.logout_btn.setText("Logout")
        self.logout_btn.setFont(QtGui.QFont("", 12))
        self.logout_btn.setStyleSheet("color: rgb(154, 153, 150); padding: 5px 10px;")
        self.logout_btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
        self.logout_btn.mousePressEvent = lambda e: showLogin()
        self.logout_btn.enterEvent = lambda e: self.logout_btn.setStyleSheet("color: rgb(255, 255, 255); padding: 5px 10px;")
        self.logout_btn.leaveEvent = lambda e: self.logout_btn.setStyleSheet("color: rgb(154, 153, 150); padding: 5px 10px;")
        self.topbar.addWidget(self.logout_btn)

        self.curr_label = create_lines(self)
        self.mistakes = 0
        self.typed_words = 0
        self.total_letters = 0
        self.incorrect = 0
        self.last_len = 0
        self.type.textChanged.connect(self.text_change)

        self.type.setText("")
        self.text_lines = generate_words()


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(200)
        self.start_time = None
        self.chose_time = 30
        self.time.setText(f"Time left: {self.chose_time}s")

        self.time_buttons = []
        time_btn_style = "color: rgb(154, 153, 150); background-color: rgba(255,255,255,0); padding: 2px 8px; font-size: 14px;"
        time_btn_active = "color: rgb(255, 255, 255); background-color: rgba(82, 0, 255, 80); padding: 2px 8px; font-size: 14px; border-radius: 4px;"
        for idx, t in enumerate([15, 30, 60, 120]):
            btn = QLabel(self)
            btn.setText(f"{t}s")
            btn.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(time_btn_active if t == 30 else time_btn_style)
            btn.mousePressEvent = lambda e, sec=t: self.set_time(sec)
            self.time_buttons.append((btn, t))
            self.panel.insertWidget(1 + idx, btn)

        self.pointer_timer = QTimer(self)
        self.pointer_timer.timeout.connect(self.blink_pointer)
        self.pointer_timer.start(500)
        self.pointer_anim = QPropertyAnimation(self.pointer, b"pos")
        self.pointer_anim.setDuration(150)

        QTimer.singleShot(0, self.update_labels)

    def set_time(self, seconds):
        if self.start_time is not None:
            return
        self.chose_time = seconds
        self.time.setText(f"Time left: {self.chose_time}s")
        time_btn_style = "color: rgb(154, 153, 150); background-color: rgba(255,255,255,0); padding: 2px 8px; font-size: 14px;"
        time_btn_active = "color: rgb(255, 255, 255); background-color: rgba(82, 0, 255, 80); padding: 2px 8px; font-size: 14px; border-radius: 4px;"
        for btn, t in self.time_buttons:
            btn.setStyleSheet(time_btn_active if t == seconds else time_btn_style)

    def blink_pointer(self):
        self.pointer.setVisible(not self.pointer.isVisible())

    def move_pointer(self, label: QLabel):
        target_pos = label.mapTo(self, QPoint(0, 0))
        target_pos.setX(target_pos.x() - 1)
        target_pos.setY(target_pos.y() + 2)

        self.pointer_anim.setStartValue(self.pointer.pos())
        self.pointer_anim.setEndValue(target_pos)
        self.pointer_anim.start()

    def text_change(self):
        self.typed = self.type.text()
        self.start()
        self.pointer_timer.stop()
        self.pointer.setVisible(True)
        should_check_correctness = False
        if len(self.typed) >= len(self.text_lines[0]) + len(self.text_lines[1]):
            should_check_correctness = True
            word_correct = True
            for i in range(len(self.text_lines[0])):
                if self.text_lines[0][i] == " ":
                    if word_correct:
                        self.typed_words += 1
                    word_correct = True
                    continue
                if self.typed[i] != self.text_lines[0][i]:
                    self.mistakes += 1
                    word_correct = False
            self.total_letters += len(self.text_lines[0]) - self.text_lines[0].count(" ")
            self.typed = self.typed[len(self.text_lines[0]):]
            self.type.setText(self.typed)
            self.text_lines.pop(0)
        else:
            if self.last_len < len(self.typed):
                should_check_correctness = True

        self.update_labels()
        self.last_len = len(self.typed)
        if not should_check_correctness:
            return

        if len(self.typed) > len(self.text_lines[0]):
            if self.typed[-1] != self.text_lines[1][len(self.typed) - len(self.text_lines[0]) - 1]:
                self.incorrect += 1
        else:
            if self.typed[-1] != self.text_lines[0][len(self.typed) - 1]:
                self.incorrect += 1


    def update_labels(self):
        t_i = 0
        for i in range(self.lines.count()):
            line = self.lines.itemAt(i)

            if not isinstance(line, QHBoxLayout):
                continue

            s_i = 0
            for j in range(line.count()):
                char_item = line.itemAt(j)

                if not isinstance(char_item, QWidgetItem):
                    continue

                if isinstance(char_item, QSpacerItem):
                    continue

                char = char_item.widget()
                if not isinstance(char, QLabel):
                    continue

                if s_i >= len(self.text_lines[i]):
                    char.setText(" ")
                    continue

                char.setText(self.text_lines[i][s_i])
                if t_i >= len(self.typed):
                    char.setStyleSheet(inactive_stylesheet)

                    if t_i == len(self.typed):
                        t_i += 1
                        self.curr_label = char
                else:
                    if self.typed[t_i] == self.text_lines[i][s_i]:
                        char.setStyleSheet(active_stylesheet)
                    elif self.text_lines[i][s_i] != " ":
                        char.setStyleSheet(incorrect_stylesheet)
                    else:
                        char.setStyleSheet(incorrect_stylesheet)
                        char.setText(self.typed[t_i])
                    t_i += 1
                s_i += 1


    def start(self):
        if self.start_time is None:
            self.start_time = time.time() + self.chose_time

    def update(self):
        self.type.setFocus()
        self.move_pointer(self.curr_label)
        if self.start_time is not None:
            self.time_left = self.start_time - time.time()
            if self.time_left <= 0:
                window.setCentralWidget(self.stop())
                return
            self.time.setText(f"Time left: {self.time_left:.0f}s")

    def stop(self):
        if self.start_time is None:
            return

        word_correct = True

        for i in range(len(self.text_lines[0])):
            if self.text_lines[0][i] == " ":
                if word_correct:
                    self.typed_words += 1
                word_correct = True
                continue
            if i >= len(self.typed):
                self.total_letters += i - self.text_lines[0][:i].count(" ")
                return Result(self.typed_words, self.total_letters, self.chose_time, self.incorrect)
            if self.typed[i] != self.text_lines[0][i]:
                self.mistakes += 1
                word_correct = False

        self.total_letters += len(self.text_lines[0]) - self.text_lines[0].count(" ")

        offset = len(self.text_lines[0])
        for i in range(len(self.text_lines[1])):
            if self.text_lines[1][i] == " ":
                if word_correct:
                    self.typed_words += 1
                word_correct = True
                continue
            if i + offset >= len(self.typed):
                self.total_letters += i - self.text_lines[1][:i].count(" ")
                return Result(self.typed_words, self.total_letters, self.chose_time, self.incorrect)
            if self.typed[i + offset] != self.text_lines[1][i]:
                self.mistakes += 1
                word_correct = False

        self.total_letters += len(self.text_lines[1]) - self.text_lines[1].count(" ")

        return Result(self.typed_words, self.total_letters, self.chose_time, self.incorrect)

class Result(QWidget):
    def __init__(self, words: int, letters: int, time: float, incorrects: int):
        super().__init__()
        uic.loadUi(path("ui/result.ui"), self)
        wpm_val = words / time * 60 if time > 0 else 0
        acc = (letters - incorrects) / letters * 100 if letters > 0 else 0
        self.wpm.setText(headedStr(f"{wpm_val:.0f} wpm", 1))
        self.stats.setText(f"{words} words\n{time:.0f} seconds\n{acc:.0f}% accuracy")
        self.try_again: QLabel
        self.try_again.mousePressEvent = lambda e: login()
        self.try_again.enterEvent = lambda e: self.try_again.setStyleSheet("color: rgb(255, 255, 255);")
        self.try_again.leaveEvent = lambda e: self.try_again.setStyleSheet("color: rgb(154, 153, 150);")

        self.bottom: QHBoxLayout
        dman.add_data(username, wpm_val, acc)
        data = dman.get_data(username)
        self.bottom.addWidget(StatsGraph(data["wpm"], data["accuracy"]))

class StatsGraph(QWidget):
    def __init__(self, wpm_data: list[float], acc_data: list[float]):
        super().__init__()

        if len(wpm_data) == 1:
            wpm_data.append(wpm_data[0])
            acc_data.append(acc_data[0])

        layout = QVBoxLayout(self)
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)

        view = self.plot.getViewBox()

        view.setMouseEnabled(x=False, y=False)
        view.setMenuEnabled(False)
        view.setLimits(
            xMin=0,
            xMax=len(wpm_data) - 1,
            yMin=0,
            yMax=300,
        )
        view.setDefaultPadding(0)
        self.plot.setXRange(0, len(wpm_data) - 1, padding=0)

        WPM_COLOR = (90, 200, 255)
        ACC_COLOR = (120, 255, 120)

        left_axis = self.plot.getAxis("left")
        right_axis = self.plot.getAxis("right")
        self.plot.showAxis("right")
        self.plot.getAxis("bottom").hide()

        left_axis.setLabel("WPM", color=WPM_COLOR)
        left_axis.setPen(pg.mkPen(WPM_COLOR))
        left_axis.setTextPen(pg.mkPen(WPM_COLOR))

        right_axis.setLabel("Accuracy %", color=ACC_COLOR)
        right_axis.setPen(pg.mkPen(ACC_COLOR))
        right_axis.setTextPen(pg.mkPen(ACC_COLOR))

        self.plot.setBackground((36, 31, 49))

        self.wpm_curve = self.plot.plot(
            wpm_data,
            pen=pg.mkPen((WPM_COLOR), width=3),
        )

        self.acc_view = pg.ViewBox()
        self.acc_view.setXLink(self.plot)
        self.acc_view.setMouseEnabled(x=False, y=False)
        self.acc_view.setMenuEnabled(False)
        self.acc_view.setLimits(
           yMin=0,
           yMax=100
        )

        self.plot.scene().addItem(self.acc_view)
        right_axis.linkToView(self.acc_view)

        self.acc_curve = pg.PlotCurveItem(
            acc_data,
            pen=pg.mkPen((ACC_COLOR), width=3),
        )
        self.acc_view.addItem(self.acc_curve)

        view.sigResized.connect(self.update_views)
        self.update_views()

        self.plot.setYRange(0, 300)
        self.acc_view.setYRange(0, 100)
        self.plot.setXRange(0, len(wpm_data) - 1, padding=0)

    def update_views(self):
        self.acc_view.setGeometry(self.plot.getViewBox().sceneBoundingRect())
        self.acc_view.linkedViewChanged(self.plot.getViewBox(), self.acc_view.XAxis)


dman = DataManager(TLDS)

app = QApplication([])
app.setWindowIcon(QIcon("icon.png"))
window = QMainWindow()
window.setStyleSheet("background-color: rgb(36, 31, 49);")
window.setWindowTitle("Lypa - Typing Test Application")

showLogin()
window.showMaximized()


sys.exit(app.exec())
