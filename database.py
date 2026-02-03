import sqlite3
import os


class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'school.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._insert_sample_data()

    def _create_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fullname TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                student_code TEXT,
                fullname TEXT NOT NULL,
                class_name TEXT,
                school_year TEXT,
                date_of_birth TEXT,
                gender TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject_id INTEGER,
                exam_type TEXT,
                score REAL,
                semester INTEGER DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            );
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject_id INTEGER,
                day_of_week INTEGER,
                period INTEGER,
                room TEXT,
                teacher TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            );
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                ntype TEXT DEFAULT 'school',
                date_posted TEXT,
                is_read INTEGER DEFAULT 0
            );
        ''')
        self.conn.commit()

    def _insert_sample_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] > 0:
            return

        # Default user
        self.cursor.execute(
            "INSERT INTO users (email, password, fullname) VALUES (?, ?, ?)",
            ("emailcuaA@gmail.com", "366761", "Nguyễn Văn Dũng")
        )
        uid = self.cursor.lastrowid

        # Student profile
        self.cursor.execute(
            "INSERT INTO students (user_id, student_code, fullname, class_name, school_year, date_of_birth, gender) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (uid, "HS20250001", "Nguyễn Văn Dũng", "12A1", "2025 - 2026", "15/05/2008", "Nam")
        )
        sid = self.cursor.lastrowid

        # Subjects
        subjects = [
            ("Toán", "TOAN"), ("Ngữ Văn", "VAN"), ("Tiếng Anh", "ANH"),
            ("Vật Lý", "LY"), ("Hóa Học", "HOA"), ("Sinh Học", "SINH"),
            ("Lịch Sử", "SU"), ("Địa Lý", "DIA"), ("GDCD", "GDCD"),
            ("Tin Học", "TIN"), ("Thể Dục", "TD"), ("Công Nghệ", "CN")
        ]
        subj_ids = {}
        for name, code in subjects:
            self.cursor.execute("INSERT INTO subjects (name, code) VALUES (?, ?)", (name, code))
            subj_ids[code] = self.cursor.lastrowid

        # Grades - điểm thực tế cho học sinh khá-giỏi ban Tự nhiên
        # Cấu trúc: { mã_môn: { học_kỳ: (Miệng, 15 phút, 1 tiết, Học kỳ) } }
        realistic_grades = {
            "TOAN":  {1: (8.0, 7.5, 8.5, 8.0), 2: (8.5, 8.0, 9.0, 8.5)},
            "VAN":   {1: (7.0, 6.5, 7.0, 6.5), 2: (7.5, 7.0, 7.0, 7.0)},
            "ANH":   {1: (8.0, 8.5, 7.5, 8.0), 2: (8.5, 8.0, 8.5, 8.5)},
            "LY":    {1: (9.0, 8.0, 8.5, 8.5), 2: (9.0, 8.5, 9.0, 9.0)},
            "HOA":   {1: (7.5, 8.0, 7.0, 7.5), 2: (8.0, 7.5, 8.0, 7.5)},
            "SINH":  {1: (7.0, 7.5, 6.5, 7.0), 2: (7.5, 7.0, 7.5, 7.0)},
            "SU":    {1: (8.0, 6.5, 7.0, 6.5), 2: (7.5, 7.0, 7.0, 7.0)},
            "DIA":   {1: (7.0, 7.0, 6.5, 7.0), 2: (7.5, 7.5, 7.0, 7.0)},
            "GDCD":  {1: (9.0, 8.5, 8.0, 8.5), 2: (9.0, 9.0, 8.5, 9.0)},
            "TIN":   {1: (9.0, 9.5, 9.0, 9.0), 2: (9.5, 10.0, 9.5, 9.5)},
            "TD":    {1: (9.0, 10.0, 9.0, 9.0), 2: (10.0, 9.0, 10.0, 9.0)},
            "CN":    {1: (8.0, 8.5, 7.5, 8.0), 2: (8.5, 8.0, 8.5, 8.0)},
        }
        exam_types = ["Miệng", "15 phút", "1 tiết", "Học kỳ"]
        for code, subj_id in subj_ids.items():
            for sem in [1, 2]:
                scores = realistic_grades[code][sem]
                for i, etype in enumerate(exam_types):
                    self.cursor.execute(
                        "INSERT INTO grades (student_id, subject_id, exam_type, score, semester) VALUES (?, ?, ?, ?, ?)",
                        (sid, subj_id, etype, scores[i], sem)
                    )

        # Thời khóa biểu chuẩn lớp 12A1 - Ban KHTN
        # Tổng: 30 tiết/tuần (Thứ 2-7, mỗi ngày 5 tiết)
        # Toán 5t, Văn 3t, Anh 4t, Lý 3t, Hóa 3t, Sinh 2t,
        # Sử 1t, Địa 1t, GDCD 1t, Tin 2t, TD 2t, CN 1t, SHL 1t, Chào cờ 1t
        schedule = [
            # Thứ 2 (Chào cờ tiết 1 → dùng GDCD thay)
            (0, 1, "GDCD", "A301", "Cô Lý Minh Trang"),
            (0, 2, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
            (0, 3, "LY",   "B102", "Th. Lê Quốc Tuấn"),
            (0, 4, "ANH",  "A301", "Cô Phạm Thùy Lan"),
            (0, 5, "HOA",  "B201", "Cô Hoàng Thị Mai"),
            # Thứ 3
            (1, 1, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
            (1, 2, "VAN",  "A301", "Cô Trần Bích Hạnh"),
            (1, 3, "ANH",  "A301", "Cô Phạm Thùy Lan"),
            (1, 4, "SINH", "B203", "Cô Ngô Thanh Thảo"),
            (1, 5, "SU",   "A301", "Th. Võ Quang Đức"),
            # Thứ 4
            (2, 1, "VAN",  "A301", "Cô Trần Bích Hạnh"),
            (2, 2, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
            (2, 3, "LY",   "B102", "Th. Lê Quốc Tuấn"),
            (2, 4, "HOA",  "A301", "Cô Hoàng Thị Mai"),
            (2, 5, "TIN",  "C101", "Th. Huỳnh Tấn Phong"),
            # Thứ 5
            (3, 1, "ANH",  "A301", "Cô Phạm Thùy Lan"),
            (3, 2, "LY",   "A301", "Th. Lê Quốc Tuấn"),
            (3, 3, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
            (3, 4, "SINH", "B203", "Cô Ngô Thanh Thảo"),
            (3, 5, "CN",   "C102", "Th. Trương Đình Long"),
            # Thứ 6
            (4, 1, "VAN",  "A301", "Cô Trần Bích Hạnh"),
            (4, 2, "HOA",  "B201", "Cô Hoàng Thị Mai"),
            (4, 3, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
            (4, 4, "ANH",  "A301", "Cô Phạm Thùy Lan"),
            (4, 5, "DIA",  "A301", "Cô Bùi Ngọc Hà"),
            # Thứ 7 (4 tiết + Sinh hoạt lớp)
            (5, 1, "TIN",  "C101", "Th. Huỳnh Tấn Phong"),
            (5, 2, "TD",   "Sân TDTT", "Th. Đỗ Mạnh Hùng"),
            (5, 3, "TD",   "Sân TDTT", "Th. Đỗ Mạnh Hùng"),
        ]
        for day, period, subj, room, teacher in schedule:
            self.cursor.execute(
                "INSERT INTO schedule (student_id, subject_id, day_of_week, period, room, teacher) VALUES (?, ?, ?, ?, ?, ?)",
                (sid, subj_ids[subj], day, period, room, teacher)
            )

        # Notifications - thông báo thực tế cho trường THPT
        notifs = [
            ("Lịch thi học kỳ I năm học 2025 - 2026",
             "Căn cứ kế hoạch năm học 2025 - 2026, nhà trường thông báo lịch thi học kỳ I như sau:\n"
             "- Khối 12: từ ngày 16/12/2025 đến 20/12/2025\n"
             "- Khối 11: từ ngày 17/12/2025 đến 21/12/2025\n"
             "- Khối 10: từ ngày 18/12/2025 đến 22/12/2025\n"
             "Học sinh ôn tập theo đề cương đã được giáo viên bộ môn phát trước đó. "
             "Lưu ý mang đầy đủ dụng cụ học tập và có mặt trước giờ thi 15 phút.",
             "school", "2025-12-01"),
            ("Họp phụ huynh học sinh học kỳ I",
             "Nhà trường kính mời quý phụ huynh học sinh lớp 12A1 tham dự buổi họp phụ huynh học kỳ I.\n"
             "- Thời gian: 8h00, Thứ Bảy ngày 28/11/2025\n"
             "- Địa điểm: Phòng học 12A1, tầng 3, dãy nhà A\n"
             "- Nội dung: Báo cáo tình hình học tập, rèn luyện của học sinh; trao đổi về công tác ôn thi tốt nghiệp THPT.\n"
             "Quý phụ huynh vui lòng sắp xếp thời gian tham dự đầy đủ.",
             "school", "2025-11-20"),
            ("Kiểm tra 1 tiết môn Toán - Lớp 12A1",
             "GVCN thông báo: Lớp 12A1 sẽ kiểm tra 1 tiết môn Toán (Đại số và Giải tích).\n"
             "- Thời gian: Tiết 3, Thứ Ba ngày 09/12/2025\n"
             "- Phạm vi: Chương I (Ứng dụng đạo hàm) và Chương II (Nguyên hàm - Tích phân)\n"
             "- Hình thức: Tự luận, thời gian 45 phút\n"
             "Các em chuẩn bị bài tốt. Thầy Nguyễn Văn Minh.",
             "teacher", "2025-11-28"),
            ("Nộp bài tập nhóm môn Ngữ Văn",
             "Cô Hạnh thông báo: Các nhóm lớp 12A1 nộp bài nghiên cứu chủ đề \"Văn học Việt Nam giai đoạn 1945-1975\".\n"
             "- Hạn nộp: Trước 17h00 ngày 10/12/2025\n"
             "- Hình thức: File Word gửi qua email cobichhanh.12a1@gmail.com hoặc nộp bản in tại phòng giáo viên\n"
             "- Yêu cầu: 8-10 trang, có trích dẫn nguồn tài liệu tham khảo\n"
             "Nhóm nào nộp trễ sẽ bị trừ 1 điểm.",
             "teacher", "2025-11-30"),
            ("Cuộc thi Tin học trẻ cấp trường năm 2025",
             "Nhà trường tổ chức cuộc thi Tin học trẻ cấp trường năm 2025 nhằm chọn đội tuyển dự thi cấp quận.\n"
             "- Thời gian thi: 7h30, Thứ Bảy ngày 20/12/2025\n"
             "- Địa điểm: Phòng máy tính số 2, dãy nhà B\n"
             "- Nội dung: Lập trình C/C++, giải thuật cơ bản\n"
             "- Đăng ký: Gặp thầy Phong (phòng Tin học) trước ngày 12/12/2025\n"
             "Khuyến khích học sinh có năng khiếu Tin học tham gia.",
             "school", "2025-12-02"),
            ("Thông báo lịch nghỉ Tết Nguyên Đán 2026",
             "Căn cứ Công văn của Sở GD&ĐT, nhà trường thông báo lịch nghỉ Tết Nguyên Đán Bính Ngọ 2026:\n"
             "- Thời gian nghỉ: Từ Thứ Bảy 24/01/2026 đến hết Chủ Nhật 02/02/2026 (10 ngày)\n"
             "- Ngày đi học lại: Thứ Hai 03/02/2026\n"
             "Trong thời gian nghỉ Tết, học sinh không tụ tập đông người, không sử dụng pháo nổ, "
             "đảm bảo an toàn giao thông và giữ gìn sức khỏe.",
             "school", "2025-12-15"),
            ("Tham quan Bảo tàng Chứng tích Chiến tranh",
             "Đoàn trường tổ chức hoạt động ngoại khóa cho học sinh khối 12.\n"
             "- Thời gian: 7h00 - 11h30, Thứ Sáu ngày 12/12/2025\n"
             "- Địa điểm: Bảo tàng Chứng tích Chiến tranh, Q.3, TP.HCM\n"
             "- Chi phí: 50.000 VNĐ/học sinh (bao gồm vé vào cổng và nước uống)\n"
             "- Đăng ký: Nộp tiền cho lớp trưởng trước ngày 08/12/2025\n"
             "Học sinh mặc đồng phục thể dục, mang theo sổ ghi chép để viết bài thu hoạch.",
             "school", "2025-12-05"),
            ("Nhắc nhở thực hiện nội quy đồng phục",
             "Ban giám hiệu nhà trường nhắc nhở toàn thể học sinh thực hiện nghiêm túc nội quy về đồng phục:\n"
             "- Thứ 2: Đồng phục trắng, thắt cà vạt (nam), nơ (nữ) - Chào cờ đầu tuần\n"
             "- Thứ 3 đến Thứ 6: Đồng phục trắng theo quy định\n"
             "- Thứ 7: Đồng phục thể dục\n"
             "Học sinh vi phạm sẽ bị nhắc nhở và trừ điểm thi đua của lớp. "
             "GVCN các lớp kiểm tra và đôn đốc học sinh thực hiện.",
             "school", "2025-11-15"),
            ("Đăng ký thi thử THPT Quốc gia lần 1",
             "Nhà trường tổ chức kỳ thi thử THPT Quốc gia lần 1 cho học sinh khối 12.\n"
             "- Thời gian thi: 06/01/2026 - 08/01/2026\n"
             "- Các bài thi: Toán, Ngữ Văn, Ngoại ngữ, Tổ hợp KHTN/KHXH\n"
             "- Lệ phí: 30.000 VNĐ/bài thi tổ hợp\n"
             "- Đăng ký tổ hợp thi: Nộp phiếu cho GVCN trước ngày 20/12/2025\n"
             "Đây là cơ hội quan trọng để các em đánh giá năng lực và điều chỉnh kế hoạch ôn tập.",
             "school", "2025-12-10"),
            ("Thay đổi phòng học môn Vật Lý",
             "Thầy Tuấn thông báo: Do phòng thí nghiệm Lý đang bảo trì, môn Vật Lý lớp 12A1 sẽ tạm thời học tại phòng 12A1 "
             "thay vì phòng thí nghiệm, áp dụng từ ngày 01/12/2025 đến khi có thông báo mới.\n"
             "Các tiết thực hành sẽ được bố trí bù sau khi phòng TN sửa chữa xong.",
             "teacher", "2025-11-29"),
        ]
        for title, content, ntype, date in notifs:
            self.cursor.execute(
                "INSERT INTO notifications (title, content, ntype, date_posted) VALUES (?, ?, ?, ?)",
                (title, content, ntype, date)
            )

        self.conn.commit()

    # ── Query methods ──────────────────────────────────────

    def authenticate(self, email, password):
        self.cursor.execute(
            "SELECT id, fullname FROM users WHERE email=? AND password=?",
            (email, password)
        )
        return self.cursor.fetchone()

    def register_user(self, fullname, email, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (email, password, fullname) VALUES (?,?,?)",
                (email, password, fullname)
            )
            uid = self.cursor.lastrowid
            self.cursor.execute(
                "INSERT INTO students (user_id, fullname, class_name, school_year) VALUES (?,?,?,?)",
                (uid, fullname, "Chưa xếp lớp", "2025 - 2026")
            )
            self.conn.commit()
            return uid
        except sqlite3.IntegrityError:
            return None

    def get_student_by_user(self, user_id):
        self.cursor.execute("SELECT * FROM students WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def get_grades(self, student_id, semester=1):
        self.cursor.execute('''
            SELECT s.name, g.exam_type, g.score
            FROM grades g JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id=? AND g.semester=?
            ORDER BY s.name,
                CASE g.exam_type
                    WHEN 'Miệng' THEN 1
                    WHEN '15 phút' THEN 2
                    WHEN '1 tiết' THEN 3
                    WHEN 'Học kỳ' THEN 4
                END
        ''', (student_id, semester))
        return self.cursor.fetchall()

    def get_schedule(self, student_id):
        self.cursor.execute('''
            SELECT sc.day_of_week, sc.period, s.name, sc.room, sc.teacher
            FROM schedule sc JOIN subjects s ON sc.subject_id = s.id
            WHERE sc.student_id=?
            ORDER BY sc.day_of_week, sc.period
        ''', (student_id,))
        return self.cursor.fetchall()

    def get_notifications(self):
        self.cursor.execute(
            "SELECT id, title, content, ntype, date_posted, is_read FROM notifications ORDER BY date_posted DESC"
        )
        return self.cursor.fetchall()

    def get_unread_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM notifications WHERE is_read=0")
        return self.cursor.fetchone()[0]

    def mark_read(self, nid):
        self.cursor.execute("UPDATE notifications SET is_read=1 WHERE id=?", (nid,))
        self.conn.commit()

    def close(self):
        self.conn.close()
