import streamlit as st
import json
import os
from datetime import datetime

# ==================== CONFIG ====================
st.set_page_config(
    page_title="LỜI NHẮC - Task Manager",
    page_icon="📋",
    layout="centered"
)

DATA_FILE = "tasks.json"
USERS_FILE = "users.json"

# ==================== STYLE ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .main-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .task-high { color: #f44336; font-weight: bold; }
    .task-medium { color: #ff9800; }
    .task-low { color: #2196f3; }
    .task-done { color: #4caf50; text-decoration: line-through; }
    .task-overdue { color: #f44336; background: #ffebee; padding: 5px; border-radius: 5px; }
    .task-soon { color: #ff9800; background: #fff3e0; padding: 5px; border-radius: 5px; }
    .counter-done {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    .counter-todo {
        background: #fff3e0;
        color: #ef6c00;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ==================== HELPER FUNCTIONS ====================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("tasks", [])
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=2)


def validate_email(email):
    email = email.strip()
    if not email:
        return False, "Email không được để trống!"
    if "@" not in email or email.count("@") != 1:
        return False, "Email không hợp lệ. Ví dụ: example@gmail.com"
    if email.startswith("@") or email.endswith("@"):
        return False, "Email không hợp lệ!"
    return True, ""


def get_task_status(task_time_str):
    """Trả về trạng thái: overdue, soon, normal"""
    try:
        task_time = datetime.strptime(task_time_str, "%Y-%m-%d %H:%M")
        now = datetime.now()
        diff_minutes = (task_time - now).total_seconds() / 60

        if diff_minutes < 0:
            return "overdue"
        elif diff_minutes <= 10:
            return "soon"
        else:
            return "normal"
    except:
        return "normal"


# ==================== SESSION STATE ====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"


# ==================== LOGIN PAGE ====================
def login_page():
    st.markdown("<h1 style='text-align:center; color:white;'>📋 LỜI NHẮC</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#0b4f6c;'>ĐĂNG NHẬP</h2>", unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="example@gmail.com", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        remember = st.checkbox("Remember me")

        if st.button("🔐 Đăng nhập", use_container_width=True, type="primary"):
            valid, msg = validate_email(email)
            if not valid:
                st.error(msg)
            else:
                users = load_users()
                if email in users and users[email]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = users[email].get("username", email)
                    st.rerun()
                elif email not in users:
                    st.error("Email chưa được đăng ký!")
                else:
                    st.error("Sai mật khẩu!")

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📝 Tạo tài khoản", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        with col_b:
            if st.button("❓ Quên mật khẩu", use_container_width=True):
                st.info("Liên hệ admin để reset mật khẩu")

        st.markdown("</div>", unsafe_allow_html=True)


# ==================== REGISTER PAGE ====================
def register_page():
    st.markdown("<h1 style='text-align:center; color:white;'>📋 LỜI NHẮC</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#0b4f6c;'>ĐĂNG KÝ</h2>", unsafe_allow_html=True)

        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", placeholder="example@gmail.com", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        terms = st.checkbox("Tôi đồng ý với điều khoản sử dụng")

        if st.button("📝 Đăng ký", use_container_width=True, type="primary"):
            valid, msg = validate_email(email)
            if not valid:
                st.error(msg)
            elif not username.strip():
                st.error("Username không được để trống!")
            elif len(password) < 4:
                st.error("Password phải có ít nhất 4 ký tự!")
            elif password != confirm:
                st.error("Password xác nhận không khớp!")
            elif not terms:
                st.error("Bạn phải đồng ý với điều khoản!")
            else:
                users = load_users()
                if email in users:
                    st.error("Email đã được đăng ký!")
                else:
                    users[email] = {"username": username, "password": password}
                    save_users(users)
                    st.success("Đăng ký thành công! Vui lòng đăng nhập.")
                    st.session_state.page = "login"
                    st.rerun()

        st.markdown("---")
        if st.button("🔙 Đã có tài khoản? Đăng nhập", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ==================== MAIN APP ====================
def main_app():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<h1 style='color:white;'>📋 Daily Todo - {st.session_state.username}</h1>", unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # Load tasks
    tasks = load_tasks()

    # Counter
    done_count = sum(1 for t in tasks if t.get("done"))
    todo_count = len(tasks) - done_count

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='counter-done'>✅ Hoàn thành: {done_count}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='counter-todo'>⏳ Chưa hoàn thành: {todo_count}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Check for reminders
    now = datetime.now()
    for task in tasks:
        if not task.get("done") and task.get("time"):
            try:
                task_time = datetime.strptime(task["time"], "%Y-%m-%d %H:%M")
                diff = (task_time - now).total_seconds() / 60
                if -1 <= diff <= 1:
                    st.warning(f"⏰ **NHẮC VIỆC:** {task['text']} - Đến giờ rồi!")
            except:
                pass

    # Add task form
    st.subheader("➕ Thêm công việc mới")

    col1, col2 = st.columns([3, 1])
    with col1:
        new_task = st.text_input("Tên công việc", placeholder="Nhập công việc...", key="new_task")
    with col2:
        priority = st.selectbox("Độ ưu tiên", ["Cao", "Trung bình", "Thấp"])

    col1, col2 = st.columns([2, 1])
    with col1:
        task_date = st.date_input("Ngày", value=datetime.now().date())
    with col2:
        task_time = st.time_input("Giờ", value=datetime.now().time())

    if st.button("➕ Thêm công việc", use_container_width=True, type="primary"):
        if not new_task.strip():
            st.error("Vui lòng nhập tên công việc!")
        else:
            task_datetime = datetime.combine(task_date, task_time)
            tasks.append({
                "text": new_task.strip(),
                "time": task_datetime.strftime("%Y-%m-%d %H:%M"),
                "priority": priority,
                "done": False
            })
            save_tasks(tasks)
            st.success("Đã thêm công việc!")
            st.rerun()

    st.markdown("---")

    # Filter
    filter_option = st.radio("Lọc:", ["Tất cả", "Chưa hoàn thành", "Đã hoàn thành"], horizontal=True)

    # Sort tasks
    def sort_key(t):
        if t.get("done"):
            return (2, "")
        try:
            task_time = datetime.strptime(t["time"], "%Y-%m-%d %H:%M")
            return (0 if task_time < now else 1, t["time"])
        except:
            return (1, "")

    sorted_tasks = sorted(tasks, key=sort_key)

    # Display tasks
    st.subheader("📋 Danh sách công việc")

    if not sorted_tasks:
        st.info("Chưa có công việc nào. Hãy thêm công việc mới!")

    for i, task in enumerate(sorted_tasks):
        # Filter
        if filter_option == "Chưa hoàn thành" and task.get("done"):
            continue
        if filter_option == "Đã hoàn thành" and not task.get("done"):
            continue

        # Style based on status
        status = get_task_status(task.get("time", ""))
        priority = task.get("priority", "Thấp")

        # Priority icon
        if priority == "Cao":
            icon = "⚡"
        elif priority == "Trung bình":
            icon = "⭐"
        else:
            icon = "💤"

        # Display
        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            if task.get("done"):
                st.markdown(f"<p class='task-done'>✅ {icon} {task['text']} | 🕐 {task.get('time', 'N/A')}</p>", unsafe_allow_html=True)
            elif status == "overdue":
                st.markdown(f"<p class='task-overdue'>🔴 {icon} {task['text']} | 🕐 {task.get('time', 'N/A')} - QUÁ HẠN!</p>", unsafe_allow_html=True)
            elif status == "soon":
                st.markdown(f"<p class='task-soon'>🟠 {icon} {task['text']} | 🕐 {task.get('time', 'N/A')} - SẮP TỚI!</p>", unsafe_allow_html=True)
            else:
                if priority == "Cao":
                    st.markdown(f"<p class='task-high'>⚪ {icon} {task['text']} | 🕐 {task.get('time', 'N/A')}</p>", unsafe_allow_html=True)
                elif priority == "Trung bình":
                    st.markdown(f"<p class='task-medium'>⚪ {icon} {task['text']} | 🕐 {task.get('time', 'N/A')}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='task-low'>⚪ {icon} {task['text']} | 🕐 {task.get('time', 'N/A')}</p>", unsafe_allow_html=True)

        with col2:
            if not task.get("done"):
                if st.button("✅", key=f"done_{i}", help="Hoàn thành"):
                    # Find original index
                    orig_idx = tasks.index(task)
                    tasks[orig_idx]["done"] = True
                    save_tasks(tasks)
                    st.rerun()

        with col3:
            if st.button("🗑️", key=f"del_{i}", help="Xóa"):
                tasks.remove(task)
                save_tasks(tasks)
                st.rerun()

    # Clear all
    st.markdown("---")
    if st.button("🧹 Xóa tất cả công việc", type="secondary"):
        save_tasks([])
        st.rerun()


# ==================== MAIN ====================
if st.session_state.logged_in:
    main_app()
elif st.session_state.page == "register":
    register_page()
else:
    login_page()
