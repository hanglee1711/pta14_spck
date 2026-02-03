import datetime
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton,
    QButtonGroup, QStackedWidget, QScrollArea, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from icons import Icons


# ════════════════════════════════════════════════════════════
#  Stylesheet
# ════════════════════════════════════════════════════════════
STYLE = """
QWidget#dashboard {
    background-color: #F0F7FF;
    font-family: 'Segoe UI', Arial, sans-serif;
}
#sidebar {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}
#studentCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #3B82F6, stop:0.5 #6366F1, stop:1 #8B5CF6);
    border-radius: 16px;
}
#studentName {
    color: white; font-size: 16px; font-weight: bold;
}
#studentInfo {
    color: rgba(255,255,255,200); font-size: 12px;
}
#navBtn {
    background: transparent; border: none; border-radius: 12px;
    padding: 13px 16px; text-align: left;
    font-size: 14px; font-weight: 500; color: #64748B;
}
#navBtn:hover {
    background-color: #F1F5F9; color: #334155;
}
#navBtn:checked {
    background-color: #3B82F6; color: white; font-weight: 600;
}
#logoutBtn {
    background: transparent; border: 2px solid #FEE2E2; border-radius: 12px;
    padding: 11px 16px; text-align: left;
    font-size: 14px; color: #EF4444; font-weight: 500;
}
#logoutBtn:hover {
    background-color: #FEF2F2; border-color: #FECACA;
}
#contentArea {
    background-color: #F0F7FF;
}
#contentTitle {
    font-size: 22px; font-weight: bold; color: #1E293B;
}
#statCard {
    background: white; border-radius: 14px;
    padding: 16px; border: 1px solid #E2E8F0;
}
#statNumber {
    font-size: 26px; font-weight: bold;
}
#statLabel {
    font-size: 12px; color: #64748B; font-weight: 500;
}
#sectionLabel {
    font-size: 16px; font-weight: 600; color: #334155;
    padding: 6px 0px 2px 0px;
}
#notifCard {
    background: white; border-radius: 12px;
    padding: 13px 16px; border: 1px solid #E2E8F0;
}
#notifCard:hover {
    border-color: #93C5FD;
}
#notifTitle {
    font-size: 13px; font-weight: 600; color: #1E293B;
}
#notifDate {
    font-size: 11px; color: #94A3B8;
}
#notifContent {
    font-size: 12px; color: #64748B;
}
QTableWidget {
    background: white; border-radius: 12px;
    border: 1px solid #E2E8F0; gridline-color: #F1F5F9;
    font-size: 13px;
}
QTableWidget::item { padding: 6px; }
QHeaderView::section {
    background: #F8FAFC; padding: 10px; border: none;
    border-bottom: 2px solid #E2E8F0;
    font-weight: 600; color: #475569; font-size: 13px;
}
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical {
    background: transparent; width: 8px;
}
QScrollBar::handle:vertical {
    background: #CBD5E1; border-radius: 4px; min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #94A3B8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
QComboBox {
    padding: 8px 14px; border: 2px solid #E2E8F0; border-radius: 10px;
    background: white; font-size: 13px; min-width: 140px;
}
QComboBox:hover { border-color: #93C5FD; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox QAbstractItemView {
    border: 1px solid #E2E8F0; border-radius: 8px;
    background: white; selection-background-color: #EFF6FF;
    selection-color: #1E293B;
}
"""

# Subject colors for schedule
SUBJECT_COLORS = {
    "Toán": "#3B82F6", "Ngữ Văn": "#10B981", "Tiếng Anh": "#8B5CF6",
    "Vật Lý": "#F59E0B", "Hóa Học": "#EF4444", "Sinh Học": "#14B8A6",
    "Lịch Sử": "#A16207", "Địa Lý": "#06B6D4", "GDCD": "#EC4899",
    "Tin Học": "#6366F1", "Thể Dục": "#22C55E", "Công Nghệ": "#78716C",
}


class DashboardWidget(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, db, user_id, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboard")
        self.db = db
        self.user_id = user_id
        self.student = db.get_student_by_user(user_id)
        self.setStyleSheet(STYLE)
        self._build()

    # ── Main layout ────────────────────────────────────────

    def _build(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._sidebar())
        root.addWidget(self._content(), 1)

    # ── Sidebar ────────────────────────────────────────────

    def _sidebar(self):
        frame = QFrame()
        frame.setObjectName("sidebar")
        frame.setFixedWidth(290)

        lay = QVBoxLayout(frame)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(6)

        lay.addWidget(self._student_card())
        lay.addSpacing(10)

        self._nav_btns = []
        grp = QButtonGroup(self)
        grp.setExclusive(True)

        nav_items = [
            ("  Trang chủ", Icons.home(24)),
            ("  Kiểm tra", Icons.exam(24)),
            ("  Lịch học", Icons.calendar(24)),
            ("  Thông báo", Icons.bell(24)),
        ]
        for i, (text, icon) in enumerate(nav_items):
            btn = QPushButton(text)
            btn.setIcon(icon)
            btn.setIconSize(QSize(24, 24))
            btn.setCheckable(True)
            btn.setObjectName("navBtn")
            btn.setMinimumHeight(46)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=i: self._go(idx))
            grp.addButton(btn)
            lay.addWidget(btn)
            self._nav_btns.append(btn)

        self._nav_btns[0].setChecked(True)
        lay.addStretch()

        logout = QPushButton("  Đăng xuất")
        logout.setIcon(Icons.logout(24))
        logout.setIconSize(QSize(24, 24))
        logout.setObjectName("logoutBtn")
        logout.setMinimumHeight(46)
        logout.setCursor(Qt.CursorShape.PointingHandCursor)
        logout.clicked.connect(self.logout_requested.emit)
        lay.addWidget(logout)

        return frame

    def _student_card(self):
        card = QFrame()
        card.setObjectName("studentCard")
        card.setMinimumHeight(108)

        lay = QHBoxLayout(card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(14)

        avatar = QLabel()
        avatar.setFixedSize(70, 70)
        avatar.setPixmap(Icons.person_avatar(70))
        lay.addWidget(avatar)

        info = QVBoxLayout()
        info.setSpacing(2)

        s = self.student
        name = s[3] if s else "Học sinh"
        cls = s[4] if s else "N/A"
        year = s[5] if s else "N/A"
        code = s[2] if s and s[2] else ""

        n = QLabel(name)
        n.setObjectName("studentName")
        info.addWidget(n)
        for txt in [f"Lớp: {cls}", f"Niên khóa: {year}"] + ([f"MSS: {code}"] if code else []):
            l = QLabel(txt)
            l.setObjectName("studentInfo")
            info.addWidget(l)
        info.addStretch()
        lay.addLayout(info)
        lay.addStretch()
        return card

    # ── Content area ───────────────────────────────────────

    def _content(self):
        frame = QFrame()
        frame.setObjectName("contentArea")
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(26, 20, 26, 20)
        lay.setSpacing(10)

        self._title = QLabel("Thông tin nổi bật")
        self._title.setObjectName("contentTitle")
        lay.addWidget(self._title)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._page_home())
        self._stack.addWidget(self._page_exam())
        self._stack.addWidget(self._page_schedule())
        self._stack.addWidget(self._page_notify())
        lay.addWidget(self._stack)
        return frame

    def _go(self, idx):
        self._stack.setCurrentIndex(idx)
        titles = ["Thông tin nổi bật", "Kết quả kiểm tra", "Thời khóa biểu", "Thông báo"]
        self._title.setText(titles[idx])
        if idx == 1:
            self._load_grades()
        elif idx == 2:
            self._load_schedule()
        elif idx == 3:
            self._load_notifications()

    # ── HOME page ──────────────────────────────────────────

    def _page_home(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        page = QWidget()
        page.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(page)
        lay.setSpacing(12)
        lay.setContentsMargins(0, 0, 6, 0)

        # Stats row
        sid = self.student[0] if self.student else 0
        grades = self.db.get_grades(sid)
        avg = sum(g[2] for g in grades) / len(grades) if grades else 0
        unread = self.db.get_unread_count()

        row = QHBoxLayout()
        row.setSpacing(12)
        row.addWidget(self._stat("Điểm TB", f"{avg:.1f}", "#3B82F6"))
        row.addWidget(self._stat("Môn học", "12", "#10B981"))
        row.addWidget(self._stat("Thông báo mới", str(unread), "#F59E0B"))
        lay.addLayout(row)

        # Recent notifications
        lay.addWidget(self._section("Thông báo mới nhất"))
        for n in self.db.get_notifications()[:3]:
            lay.addWidget(self._notif_card(n))

        # Today's schedule
        lay.addWidget(self._section("Lịch học hôm nay"))
        lay.addWidget(self._today())

        lay.addStretch()
        scroll.setWidget(page)
        return scroll

    def _stat(self, label, value, color):
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumHeight(85)
        lay = QVBoxLayout(card)
        lay.setSpacing(4)
        bar = QFrame()
        bar.setFixedHeight(4)
        bar.setStyleSheet(f"background:{color}; border-radius:2px;")
        lay.addWidget(bar)
        v = QLabel(value)
        v.setObjectName("statNumber")
        v.setStyleSheet(f"color:{color};")
        lay.addWidget(v)
        l = QLabel(label)
        l.setObjectName("statLabel")
        lay.addWidget(l)
        return card

    def _section(self, text):
        l = QLabel(text)
        l.setObjectName("sectionLabel")
        return l

    def _notif_card(self, n):
        card = QFrame()
        card.setObjectName("notifCard")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        lay = QHBoxLayout(card)
        lay.setSpacing(10)

        dot = QLabel()
        dot.setFixedSize(10, 10)
        c = "#3B82F6" if n[3] == "school" else "#10B981"
        dot.setStyleSheet(f"background:{c}; border-radius:5px;")
        lay.addWidget(dot, 0, Qt.AlignmentFlag.AlignTop)

        col = QVBoxLayout()
        col.setSpacing(2)
        hdr = QHBoxLayout()
        t = QLabel(n[1])
        t.setObjectName("notifTitle")
        t.setWordWrap(True)
        hdr.addWidget(t, 1)
        d = QLabel(n[4])
        d.setObjectName("notifDate")
        hdr.addWidget(d)
        col.addLayout(hdr)

        txt = n[2]
        preview = QLabel(txt[:100] + "..." if len(txt) > 100 else txt)
        preview.setObjectName("notifContent")
        preview.setWordWrap(True)
        col.addWidget(preview)
        lay.addLayout(col, 1)
        return card

    def _today(self):
        today = datetime.datetime.now().weekday()
        if today > 5:
            today = 0

        sid = self.student[0] if self.student else 0
        all_sch = self.db.get_schedule(sid)
        classes = [(s[1], s[2], s[3], s[4]) for s in all_sch if s[0] == today]

        card = QFrame()
        card.setObjectName("statCard")
        lay = QVBoxLayout(card)

        if not classes:
            l = QLabel("Không có lịch học hôm nay")
            l.setStyleSheet("color:#94A3B8; padding:16px; font-style:italic;")
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lay.addWidget(l)
            return card

        days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"]
        dl = QLabel(days[today])
        dl.setStyleSheet("font-weight:600; color:#3B82F6; font-size:14px; padding-bottom:4px;")
        lay.addWidget(dl)

        for period, subj, room, teacher in classes:
            r = QHBoxLayout()
            r.setSpacing(12)

            p_lbl = QLabel(f"Tiết {period}")
            p_lbl.setFixedWidth(50)
            p_lbl.setStyleSheet("color:#94A3B8; font-weight:500;")

            sc = SUBJECT_COLORS.get(subj, "#64748B")
            s_lbl = QLabel(subj)
            s_lbl.setFixedWidth(100)
            s_lbl.setStyleSheet(f"font-weight:600; color:{sc};")

            rm = QLabel(room)
            rm.setFixedWidth(90)
            rm.setStyleSheet("color:#64748B;")

            tc = QLabel(teacher)
            tc.setStyleSheet("color:#64748B;")

            r.addWidget(p_lbl)
            r.addWidget(s_lbl)
            r.addWidget(rm)
            r.addWidget(tc)
            r.addStretch()
            lay.addLayout(r)

        return card

    # ── EXAM page ──────────────────────────────────────────

    def _page_exam(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setSpacing(12)
        lay.setContentsMargins(0, 0, 0, 0)

        hdr = QHBoxLayout()
        lbl = QLabel("Học kỳ:")
        lbl.setStyleSheet("font-weight:600; font-size:14px;")
        hdr.addWidget(lbl)
        self._sem = QComboBox()
        self._sem.addItems(["Học kỳ I", "Học kỳ II"])
        self._sem.currentIndexChanged.connect(lambda: self._load_grades())
        hdr.addWidget(self._sem)
        hdr.addStretch()
        lay.addLayout(hdr)

        self._grade_tbl = QTableWidget()
        self._grade_tbl.setColumnCount(6)
        self._grade_tbl.setHorizontalHeaderLabels(
            ["Môn học", "Miệng", "15 phút", "1 tiết", "Học kỳ", "TB Môn"]
        )
        self._grade_tbl.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        for i in range(1, 6):
            self._grade_tbl.horizontalHeader().setSectionResizeMode(
                i, QHeaderView.ResizeMode.ResizeToContents
            )
        self._grade_tbl.verticalHeader().setVisible(False)
        self._grade_tbl.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._grade_tbl.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._grade_tbl.setAlternatingRowColors(True)
        self._grade_tbl.setStyleSheet("alternate-background-color: #F8FAFC;")
        lay.addWidget(self._grade_tbl, 1)

        summary = QFrame()
        summary.setObjectName("statCard")
        sl = QHBoxLayout(summary)
        self._avg_lbl = QLabel("Điểm trung bình: --")
        self._avg_lbl.setStyleSheet("font-size:15px; font-weight:600; color:#3B82F6;")
        self._rank_lbl = QLabel("Học lực: --")
        self._rank_lbl.setStyleSheet("font-size:15px; font-weight:600; color:#10B981;")
        sl.addWidget(self._avg_lbl)
        sl.addStretch()
        sl.addWidget(self._rank_lbl)
        lay.addWidget(summary)

        self._load_grades()
        return page

    def _load_grades(self):
        sem = self._sem.currentIndex() + 1
        sid = self.student[0] if self.student else 0
        rows = self.db.get_grades(sid, sem)

        subjects = {}
        for name, etype, score in rows:
            if name not in subjects:
                subjects[name] = {}
            subjects[name][etype] = score

        self._grade_tbl.setRowCount(len(subjects))
        total, cnt = 0, 0
        etypes = ["Miệng", "15 phút", "1 tiết", "Học kỳ"]
        weights = [1, 1, 2, 3]

        for row, (subj, scores) in enumerate(sorted(subjects.items())):
            self._grade_tbl.setItem(row, 0, QTableWidgetItem(subj))

            vals = []
            for col, et in enumerate(etypes):
                sc = scores.get(et)
                if sc is not None:
                    item = QTableWidgetItem(f"{sc:.1f}")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setForeground(self._score_color(sc))
                    self._grade_tbl.setItem(row, col + 1, item)
                    vals.append(sc)

            if len(vals) == 4:
                avg = sum(v * w for v, w in zip(vals, weights)) / sum(weights)
            elif vals:
                avg = sum(vals) / len(vals)
            else:
                avg = 0

            ai = QTableWidgetItem(f"{avg:.1f}")
            ai.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ai.setForeground(self._score_color(avg))
            f = ai.font()
            f.setBold(True)
            ai.setFont(f)
            self._grade_tbl.setItem(row, 5, ai)
            total += avg
            cnt += 1

        if cnt:
            oa = total / cnt
            self._avg_lbl.setText(f"Điểm trung bình: {oa:.2f}")
            if oa >= 8:
                r, c = "Giỏi", "#10B981"
            elif oa >= 6.5:
                r, c = "Khá", "#3B82F6"
            elif oa >= 5:
                r, c = "Trung bình", "#F59E0B"
            else:
                r, c = "Yếu", "#EF4444"
            self._rank_lbl.setText(f"Học lực: {r}")
            self._rank_lbl.setStyleSheet(f"font-size:15px; font-weight:600; color:{c};")

    @staticmethod
    def _score_color(s):
        if s >= 8:
            return QColor("#10B981")
        if s >= 6.5:
            return QColor("#3B82F6")
        if s >= 5:
            return QColor("#F59E0B")
        return QColor("#EF4444")

    # ── SCHEDULE page ──────────────────────────────────────

    def _page_schedule(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setSpacing(12)
        lay.setContentsMargins(0, 0, 0, 0)

        # Tiêu đề phụ
        info = QLabel("Lớp 12A1 - Học kỳ I - Năm học 2025-2026")
        info.setStyleSheet("font-size:13px; color:#64748B; font-weight:500; padding:2px 0;")
        lay.addWidget(info)

        self._sch_tbl = QTableWidget()
        self._sch_tbl.setColumnCount(6)
        self._sch_tbl.setRowCount(5)
        self._sch_tbl.setHorizontalHeaderLabels(
            ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"]
        )
        self._sch_tbl.setVerticalHeaderLabels(
            ["Tiết 1\n(7:00)", "Tiết 2\n(7:50)", "Tiết 3\n(8:40)", "Tiết 4\n(9:40)", "Tiết 5\n(10:30)"]
        )
        self._sch_tbl.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._sch_tbl.horizontalHeader().setMinimumSectionSize(120)
        for r in range(5):
            self._sch_tbl.setRowHeight(r, 80)
        self._sch_tbl.verticalHeader().setDefaultSectionSize(80)
        self._sch_tbl.verticalHeader().setMinimumWidth(70)
        self._sch_tbl.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._sch_tbl.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._sch_tbl.setStyleSheet("""
            QTableWidget {
                background: white; border-radius: 12px;
                border: 1px solid #E2E8F0; gridline-color: #E2E8F0;
                font-size: 12px;
            }
            QTableWidget::item { padding: 4px; }
            QHeaderView::section {
                background: #F1F5F9; padding: 8px; border: none;
                border-bottom: 2px solid #E2E8F0; border-right: 1px solid #E2E8F0;
                font-weight: 600; color: #475569; font-size: 12px;
            }
        """)
        lay.addWidget(self._sch_tbl, 1)

        # Legend - 2 hàng
        legend_frame = QFrame()
        legend_frame.setObjectName("statCard")
        legend_lay = QVBoxLayout(legend_frame)
        legend_lay.setSpacing(6)
        lbl = QLabel("Chú thích môn học:")
        lbl.setStyleSheet("font-weight:600; color:#475569; font-size:12px;")
        legend_lay.addWidget(lbl)

        items = list(SUBJECT_COLORS.items())
        for start in range(0, len(items), 6):
            row_lay = QHBoxLayout()
            row_lay.setSpacing(10)
            for subj, color in items[start:start+6]:
                dot = QLabel()
                dot.setFixedSize(10, 10)
                dot.setStyleSheet(f"background:{color}; border-radius:5px;")
                row_lay.addWidget(dot)
                sl = QLabel(subj)
                sl.setStyleSheet("font-size:11px; color:#64748B;")
                row_lay.addWidget(sl)
                row_lay.addSpacing(4)
            row_lay.addStretch()
            legend_lay.addLayout(row_lay)
        lay.addWidget(legend_frame)

        self._load_schedule()
        return page

    def _load_schedule(self):
        sid = self.student[0] if self.student else 0
        data = self.db.get_schedule(sid)

        # Xóa hết widget cũ
        for r in range(5):
            for c in range(6):
                self._sch_tbl.removeCellWidget(r, c)
                self._sch_tbl.setItem(r, c, QTableWidgetItem(""))

        for day, period, subj, room, teacher in data:
            if 0 <= day <= 5 and 1 <= period <= 5:
                sc = SUBJECT_COLORS.get(subj, "#64748B")
                bg = QColor(sc)
                bg.setAlpha(25)
                bg_str = f"rgba({bg.red()},{bg.green()},{bg.blue()},{bg.alpha()})"

                cell = QLabel()
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setText(
                    f"<div style='text-align:center;'>"
                    f"<b style='font-size:11pt; color:{sc};'>{subj}</b><br>"
                    f"<span style='font-size:8pt; color:#64748B;'>{room}</span><br>"
                    f"<span style='font-size:8pt; color:#94A3B8;'>{teacher}</span>"
                    f"</div>"
                )
                cell.setStyleSheet(
                    f"background-color: {bg_str}; border-radius: 6px; "
                    f"margin: 2px; padding: 4px;"
                )
                self._sch_tbl.setCellWidget(period - 1, day, cell)

    # ── NOTIFICATIONS page ─────────────────────────────────

    def _page_notify(self):
        self._notif_scroll = QScrollArea()
        self._notif_scroll.setWidgetResizable(True)
        self._notif_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._notif_container = QWidget()
        self._notif_container.setStyleSheet("background: transparent;")
        self._notif_lay = QVBoxLayout(self._notif_container)
        self._notif_lay.setSpacing(10)
        self._notif_lay.setContentsMargins(0, 0, 6, 0)
        self._notif_lay.addStretch()

        self._notif_scroll.setWidget(self._notif_container)
        self._load_notifications()
        return self._notif_scroll

    def _load_notifications(self):
        while self._notif_lay.count() > 1:
            item = self._notif_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for n in self.db.get_notifications():
            card = QFrame()
            card.setObjectName("notifCard")
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            cly = QVBoxLayout(card)
            cly.setSpacing(6)

            # Header
            hdr = QHBoxLayout()
            type_lbl = QLabel("Nhà trường" if n[3] == "school" else "Giáo viên")
            tc = "#3B82F6" if n[3] == "school" else "#10B981"
            type_lbl.setStyleSheet(
                f"color:white; background:{tc}; border-radius:8px; "
                f"padding:3px 10px; font-size:11px; font-weight:600;"
            )
            type_lbl.setFixedHeight(22)
            hdr.addWidget(type_lbl)
            hdr.addStretch()
            date_lbl = QLabel(n[4])
            date_lbl.setObjectName("notifDate")
            hdr.addWidget(date_lbl)
            cly.addLayout(hdr)

            title = QLabel(n[1])
            title.setObjectName("notifTitle")
            title.setStyleSheet("font-size:14px; font-weight:600; color:#1E293B;")
            title.setWordWrap(True)
            cly.addWidget(title)

            body = QLabel(n[2])
            body.setObjectName("notifContent")
            body.setWordWrap(True)
            body.setStyleSheet("font-size:13px; color:#64748B; line-height:1.4;")
            cly.addWidget(body)

            is_read = n[5]
            if not is_read:
                card.setStyleSheet(
                    "#notifCard { background:white; border-radius:12px; "
                    "padding:13px 16px; border:1px solid #93C5FD; border-left: 4px solid #3B82F6; }"
                )

            self._notif_lay.insertWidget(self._notif_lay.count() - 1, card)
