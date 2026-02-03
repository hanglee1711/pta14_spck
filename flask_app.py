from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "loi_nhac_secret_key_2024"

DATA_FILE = "tasks.json"
USERS_FILE = "users.json"


# ==================== HELPER ====================
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


# ==================== ROUTES ====================
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("todo"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or "@" not in email:
            error = "Email không hợp lệ!"
        else:
            users = load_users()
            if email in users and users[email]["password"] == password:
                session["user"] = email
                session["username"] = users[email].get("username", email)
                return redirect(url_for("todo"))
            elif email not in users:
                error = "Email chưa được đăng ký!"
            else:
                error = "Sai mật khẩu!"

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        terms = request.form.get("terms")

        if not username:
            error = "Username không được để trống!"
        elif not email or "@" not in email:
            error = "Email không hợp lệ!"
        elif len(password) < 4:
            error = "Password phải có ít nhất 4 ký tự!"
        elif password != confirm:
            error = "Password xác nhận không khớp!"
        elif not terms:
            error = "Bạn phải đồng ý với điều khoản!"
        else:
            users = load_users()
            if email in users:
                error = "Email đã được đăng ký!"
            else:
                users[email] = {"username": username, "password": password}
                save_users(users)
                success = "Đăng ký thành công!"

    return render_template("register.html", error=error, success=success)


@app.route("/todo")
def todo():
    if "user" not in session:
        return redirect(url_for("login"))

    tasks = load_tasks()
    now = datetime.now()

    # Sort tasks
    def sort_key(t):
        if t.get("done"):
            return (2, "")
        try:
            task_time = datetime.strptime(t["time"], "%Y-%m-%d %H:%M")
            return (0 if task_time < now else 1, t["time"])
        except:
            return (1, "")

    tasks = sorted(tasks, key=sort_key)

    # Add status to tasks
    for task in tasks:
        if task.get("done"):
            task["status"] = "done"
        elif task.get("time"):
            try:
                task_time = datetime.strptime(task["time"], "%Y-%m-%d %H:%M")
                diff = (task_time - now).total_seconds() / 60
                if diff < 0:
                    task["status"] = "overdue"
                elif diff <= 10:
                    task["status"] = "soon"
                else:
                    task["status"] = "normal"
            except:
                task["status"] = "normal"

    done_count = sum(1 for t in tasks if t.get("done"))
    todo_count = len(tasks) - done_count

    return render_template("todo.html",
                         tasks=tasks,
                         username=session.get("username", "User"),
                         done_count=done_count,
                         todo_count=todo_count)


@app.route("/add_task", methods=["POST"])
def add_task():
    if "user" not in session:
        return redirect(url_for("login"))

    text = request.form.get("task", "").strip()
    priority = request.form.get("priority", "Thấp")
    date = request.form.get("date", "")
    time = request.form.get("time", "")

    if text:
        tasks = load_tasks()
        task_time = f"{date} {time}" if date and time else ""
        tasks.append({
            "text": text,
            "time": task_time,
            "priority": priority,
            "done": False
        })
        save_tasks(tasks)

    return redirect(url_for("todo"))


@app.route("/complete_task/<int:index>")
def complete_task(index):
    if "user" not in session:
        return redirect(url_for("login"))

    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)

    return redirect(url_for("todo"))


@app.route("/delete_task/<int:index>")
def delete_task(index):
    if "user" not in session:
        return redirect(url_for("login"))

    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)

    return redirect(url_for("todo"))


@app.route("/clear_all")
def clear_all():
    if "user" not in session:
        return redirect(url_for("login"))

    save_tasks([])
    return redirect(url_for("todo"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
