import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'school.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
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
    conn.commit()

    # Insert sample data if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        insert_sample_data(conn)

    conn.close()


def insert_sample_data(conn):
    cursor = conn.cursor()

    # Default user
    cursor.execute(
        "INSERT INTO users (email, password, fullname) VALUES (?, ?, ?)",
        ("emailcuaA@gmail.com", "366761", "Nguyễn Văn Dũng")
    )
    uid = cursor.lastrowid

    # Student profile
    cursor.execute(
        "INSERT INTO students (user_id, student_code, fullname, class_name, school_year, date_of_birth, gender) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (uid, "HS20250001", "Nguyễn Văn Dũng", "12A1", "2025 - 2026", "15/05/2008", "Nam")
    )
    sid = cursor.lastrowid

    # Subjects
    subjects = [
        ("Toán", "TOAN"), ("Ngữ Văn", "VAN"), ("Tiếng Anh", "ANH"),
        ("Vật Lý", "LY"), ("Hóa Học", "HOA"), ("Sinh Học", "SINH"),
        ("Lịch Sử", "SU"), ("Địa Lý", "DIA"), ("GDCD", "GDCD"),
        ("Tin Học", "TIN"), ("Thể Dục", "TD"), ("Công Nghệ", "CN")
    ]
    subj_ids = {}
    for name, code in subjects:
        cursor.execute("INSERT INTO subjects (name, code) VALUES (?, ?)", (name, code))
        subj_ids[code] = cursor.lastrowid

    # Grades
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
                cursor.execute(
                    "INSERT INTO grades (student_id, subject_id, exam_type, score, semester) VALUES (?, ?, ?, ?, ?)",
                    (sid, subj_id, etype, scores[i], sem)
                )

    # Schedule
    schedule = [
        (0, 1, "GDCD", "A301", "Cô Lý Minh Trang"),
        (0, 2, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
        (0, 3, "LY",   "B102", "Th. Lê Quốc Tuấn"),
        (0, 4, "ANH",  "A301", "Cô Phạm Thùy Lan"),
        (0, 5, "HOA",  "B201", "Cô Hoàng Thị Mai"),
        (1, 1, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
        (1, 2, "VAN",  "A301", "Cô Trần Bích Hạnh"),
        (1, 3, "ANH",  "A301", "Cô Phạm Thùy Lan"),
        (1, 4, "SINH", "B203", "Cô Ngô Thanh Thảo"),
        (1, 5, "SU",   "A301", "Th. Võ Quang Đức"),
        (2, 1, "VAN",  "A301", "Cô Trần Bích Hạnh"),
        (2, 2, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
        (2, 3, "LY",   "B102", "Th. Lê Quốc Tuấn"),
        (2, 4, "HOA",  "A301", "Cô Hoàng Thị Mai"),
        (2, 5, "TIN",  "C101", "Th. Huỳnh Tấn Phong"),
        (3, 1, "ANH",  "A301", "Cô Phạm Thùy Lan"),
        (3, 2, "LY",   "A301", "Th. Lê Quốc Tuấn"),
        (3, 3, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
        (3, 4, "SINH", "B203", "Cô Ngô Thanh Thảo"),
        (3, 5, "CN",   "C102", "Th. Trương Đình Long"),
        (4, 1, "VAN",  "A301", "Cô Trần Bích Hạnh"),
        (4, 2, "HOA",  "B201", "Cô Hoàng Thị Mai"),
        (4, 3, "TOAN", "A301", "Th. Nguyễn Văn Minh"),
        (4, 4, "ANH",  "A301", "Cô Phạm Thùy Lan"),
        (4, 5, "DIA",  "A301", "Cô Bùi Ngọc Hà"),
        (5, 1, "TIN",  "C101", "Th. Huỳnh Tấn Phong"),
        (5, 2, "TD",   "Sân TDTT", "Th. Đỗ Mạnh Hùng"),
        (5, 3, "TD",   "Sân TDTT", "Th. Đỗ Mạnh Hùng"),
    ]
    for day, period, subj, room, teacher in schedule:
        cursor.execute(
            "INSERT INTO schedule (student_id, subject_id, day_of_week, period, room, teacher) VALUES (?, ?, ?, ?, ?, ?)",
            (sid, subj_ids[subj], day, period, room, teacher)
        )

    # Notifications
    notifs = [
        ("Lịch thi học kỳ I năm học 2025 - 2026",
         "Căn cứ kế hoạch năm học 2025 - 2026, nhà trường thông báo lịch thi học kỳ I như sau:\n- Khối 12: từ ngày 16/12/2025 đến 20/12/2025\n- Khối 11: từ ngày 17/12/2025 đến 21/12/2025\n- Khối 10: từ ngày 18/12/2025 đến 22/12/2025",
         "school", "2025-12-01"),
        ("Họp phụ huynh học sinh học kỳ I",
         "Nhà trường kính mời quý phụ huynh học sinh lớp 12A1 tham dự buổi họp phụ huynh học kỳ I.\n- Thời gian: 8h00, Thứ Bảy ngày 28/11/2025\n- Địa điểm: Phòng học 12A1, tầng 3, dãy nhà A",
         "school", "2025-11-20"),
        ("Kiểm tra 1 tiết môn Toán - Lớp 12A1",
         "GVCN thông báo: Lớp 12A1 sẽ kiểm tra 1 tiết môn Toán (Đại số và Giải tích).\n- Thời gian: Tiết 3, Thứ Ba ngày 09/12/2025\n- Phạm vi: Chương I và Chương II",
         "teacher", "2025-11-28"),
        ("Cuộc thi Tin học trẻ cấp trường năm 2025",
         "Nhà trường tổ chức cuộc thi Tin học trẻ cấp trường năm 2025.\n- Thời gian thi: 7h30, Thứ Bảy ngày 20/12/2025\n- Địa điểm: Phòng máy tính số 2, dãy nhà B",
         "school", "2025-12-02"),
        ("Thông báo lịch nghỉ Tết Nguyên Đán 2026",
         "Thời gian nghỉ: Từ Thứ Bảy 24/01/2026 đến hết Chủ Nhật 02/02/2026 (10 ngày)\nNgày đi học lại: Thứ Hai 03/02/2026",
         "school", "2025-12-15"),
    ]
    for title, content, ntype, date in notifs:
        cursor.execute(
            "INSERT INTO notifications (title, content, ntype, date_posted) VALUES (?, ?, ?, ?)",
            (title, content, ntype, date)
        )

    conn.commit()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            error = "Vui lòng nhập đầy đủ email và mật khẩu"
        else:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, fullname FROM users WHERE email=? AND password=?", (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['fullname'] = user['fullname']
                return redirect(url_for('dashboard'))
            else:
                error = "Email hoặc mật khẩu không đúng"

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not fullname or not email or not password:
            error = "Vui lòng điền đầy đủ thông tin"
        elif len(password) < 4:
            error = "Mật khẩu phải có ít nhất 4 ký tự"
        else:
            conn = get_db()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (email, password, fullname) VALUES (?,?,?)",
                    (email, password, fullname)
                )
                uid = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO students (user_id, fullname, class_name, school_year) VALUES (?,?,?,?)",
                    (uid, fullname, "Chưa xếp lớp", "2025 - 2026")
                )
                conn.commit()
                conn.close()
                return redirect(url_for('login', registered=1))
            except sqlite3.IntegrityError:
                error = "Email đã được sử dụng"
                conn.close()

    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Get student info
    cursor.execute("SELECT * FROM students WHERE user_id=?", (session['user_id'],))
    student = cursor.fetchone()

    # Get grades for average
    if student:
        cursor.execute('''
            SELECT s.name, g.exam_type, g.score
            FROM grades g JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id=? AND g.semester=1
        ''', (student['id'],))
        grades = cursor.fetchall()
        avg = sum(g['score'] for g in grades) / len(grades) if grades else 0
    else:
        avg = 0

    # Get unread notifications count
    cursor.execute("SELECT COUNT(*) as count FROM notifications WHERE is_read=0")
    unread = cursor.fetchone()['count']

    # Get recent notifications
    cursor.execute("SELECT * FROM notifications ORDER BY date_posted DESC LIMIT 3")
    notifications = cursor.fetchall()

    # Get today's schedule
    today = datetime.datetime.now().weekday()
    if today > 5:
        today = 0

    if student:
        cursor.execute('''
            SELECT sc.period, s.name, sc.room, sc.teacher
            FROM schedule sc JOIN subjects s ON sc.subject_id = s.id
            WHERE sc.student_id=? AND sc.day_of_week=?
            ORDER BY sc.period
        ''', (student['id'], today))
        today_schedule = cursor.fetchall()
    else:
        today_schedule = []

    conn.close()

    days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"]

    return render_template('dashboard.html',
                         student=student,
                         avg=avg,
                         unread=unread,
                         notifications=notifications,
                         today_schedule=today_schedule,
                         today_name=days[today],
                         page='home')


@app.route('/grades')
@login_required
def grades():
    semester = request.args.get('semester', 1, type=int)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE user_id=?", (session['user_id'],))
    student = cursor.fetchone()

    if student:
        cursor.execute('''
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
        ''', (student['id'], semester))
        grades_data = cursor.fetchall()
    else:
        grades_data = []

    conn.close()

    # Process grades
    subjects = {}
    for g in grades_data:
        name = g['name']
        if name not in subjects:
            subjects[name] = {}
        subjects[name][g['exam_type']] = g['score']

    # Calculate averages
    weights = {'Miệng': 1, '15 phút': 1, '1 tiết': 2, 'Học kỳ': 3}
    grade_list = []
    total_avg = 0

    for subj, scores in sorted(subjects.items()):
        weighted_sum = 0
        weight_total = 0
        for etype, weight in weights.items():
            if etype in scores:
                weighted_sum += scores[etype] * weight
                weight_total += weight

        avg = weighted_sum / weight_total if weight_total > 0 else 0
        grade_list.append({
            'name': subj,
            'mieng': scores.get('Miệng'),
            'p15': scores.get('15 phút'),
            'p1tiet': scores.get('1 tiết'),
            'hocky': scores.get('Học kỳ'),
            'avg': avg
        })
        total_avg += avg

    overall_avg = total_avg / len(grade_list) if grade_list else 0

    if overall_avg >= 8:
        rank = "Giỏi"
    elif overall_avg >= 6.5:
        rank = "Khá"
    elif overall_avg >= 5:
        rank = "Trung bình"
    else:
        rank = "Yếu"

    return render_template('grades.html',
                         student=student,
                         grades=grade_list,
                         overall_avg=overall_avg,
                         rank=rank,
                         semester=semester,
                         page='grades')


@app.route('/schedule')
@login_required
def schedule():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE user_id=?", (session['user_id'],))
    student = cursor.fetchone()

    if student:
        cursor.execute('''
            SELECT sc.day_of_week, sc.period, s.name, sc.room, sc.teacher
            FROM schedule sc JOIN subjects s ON sc.subject_id = s.id
            WHERE sc.student_id=?
            ORDER BY sc.day_of_week, sc.period
        ''', (student['id'],))
        schedule_data = cursor.fetchall()
    else:
        schedule_data = []

    conn.close()

    # Organize schedule into grid
    grid = [[None for _ in range(6)] for _ in range(5)]  # 5 periods x 6 days

    for s in schedule_data:
        day = s['day_of_week']
        period = s['period'] - 1
        if 0 <= day <= 5 and 0 <= period <= 4:
            grid[period][day] = {
                'name': s['name'],
                'room': s['room'],
                'teacher': s['teacher']
            }

    return render_template('schedule.html',
                         student=student,
                         schedule=grid,
                         page='schedule')


@app.route('/notifications')
@login_required
def notifications():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE user_id=?", (session['user_id'],))
    student = cursor.fetchone()

    cursor.execute("SELECT * FROM notifications ORDER BY date_posted DESC")
    notifs = cursor.fetchall()

    conn.close()

    return render_template('notifications.html',
                         student=student,
                         notifications=notifs,
                         page='notifications')


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
