import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'xnote-secret-key-2024')

USERS_FILE = "users.json"
NOTES_FILE = "notes.json"


def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ========== AUTH ROUTES ==========

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("notes"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            return render_template("login.html", error="Vui long nhap day du email va mat khau!")

        users = load_json(USERS_FILE)
        for user in users:
            if user["email"] == email and user["password"] == password:
                session["user"] = user["email"]
                session["username"] = user.get("username", "User")
                return redirect(url_for("notes"))

        return render_template("login.html", error="Email hoac mat khau khong dung!")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm", "").strip()
        terms = request.form.get("terms")

        if not username or not email or not password or not confirm:
            return render_template("register.html", error="Vui long nhap day du thong tin!")

        if password != confirm:
            return render_template("register.html", error="Mat khau xac nhan khong khop!")

        if not terms:
            return render_template("register.html", error="Ban can dong y voi dieu khoan!")

        users = load_json(USERS_FILE)
        for user in users:
            if user["email"] == email:
                return render_template("register.html", error="Email da duoc dang ky!")

        users.append({
            "username": username,
            "email": email,
            "password": password
        })
        save_json(USERS_FILE, users)

        return redirect(url_for("login", success="Dang ky thanh cong! Hay dang nhap."))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ========== NOTES ROUTES ==========

@app.route("/notes")
def notes():
    if "user" not in session:
        return redirect(url_for("login"))

    all_notes = load_json(NOTES_FILE)
    user_notes = [n for n in all_notes if n.get("user") == session["user"]]
    return render_template("notes.html", notes=user_notes, username=session.get("username", "User"))


@app.route("/api/notes", methods=["GET"])
def get_notes():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    all_notes = load_json(NOTES_FILE)
    user_notes = [n for n in all_notes if n.get("user") == session["user"]]
    return jsonify(user_notes)


@app.route("/api/notes", methods=["POST"])
def save_note():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    title = data.get("title", "").strip()
    content = data.get("content", "")
    note_id = data.get("id")

    if not title:
        return jsonify({"error": "Chua nhap tieu de"}), 400

    all_notes = load_json(NOTES_FILE)
    user_notes = [n for n in all_notes if n.get("user") == session["user"]]

    # Check duplicate title
    for i, note in enumerate(user_notes):
        if note["title"].lower() == title.lower():
            if note_id is not None and i == note_id:
                continue
            return jsonify({"error": "Tieu de ghi chu da ton tai!"}), 400

    if note_id is not None:
        # Update existing note
        count = 0
        for i, note in enumerate(all_notes):
            if note.get("user") == session["user"]:
                if count == note_id:
                    all_notes[i]["title"] = title
                    all_notes[i]["content"] = content
                    break
                count += 1
    else:
        # Add new note
        all_notes.append({
            "user": session["user"],
            "title": title,
            "content": content
        })

    save_json(NOTES_FILE, all_notes)
    return jsonify({"success": True})


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    all_notes = load_json(NOTES_FILE)
    count = 0
    for i, note in enumerate(all_notes):
        if note.get("user") == session["user"]:
            if count == note_id:
                all_notes.pop(i)
                save_json(NOTES_FILE, all_notes)
                return jsonify({"success": True})
            count += 1

    return jsonify({"error": "Note not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
