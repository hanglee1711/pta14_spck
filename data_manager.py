import sqlite3, hashlib, json, platform, os


class DataManager:
    def __init__(self, TLDS: list):
        self.TLDS = TLDS

        if platform.system() == "Windows":
            self.data_path = "data\\data.db"
            self.user_data_path = "data\\user_data.json"
        else:
            self.data_path = "data/data.db"
            self.user_data_path = "data/user_data.json"

        conn = sqlite3.connect(self.data_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, email TEXT, password TEXT)")
        conn.commit()
        conn.close()

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(32)
        hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt.hex() + "$" + hash_bytes.hex()

    def verify_password(self, password, stored):
        if "$" not in stored:
            return stored == hashlib.sha256(password.encode()).hexdigest()
        salt_hex, hash_hex = stored.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hash_bytes.hex() == hash_hex

    def _upgrade_password(self, db_username, password):
        new_hash = self.hash_password(password)
        conn = sqlite3.connect(self.data_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hash, db_username))
        conn.commit()
        conn.close()

    def register(self, username: str, email: str, password: str):
        u = username.lower()
        if not self.validate_name(u):
            return False
        if not self.validate_mail(email):
            return False
        if len(password) < 6:
            return False
        try:
            conn = sqlite3.connect(self.data_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (u, email, self.hash_password(password)))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def login(self, username: str, password: str):
        u = username.lower()
        if "@" in u:
            query = "SELECT username, password FROM users WHERE email = ?"
        else:
            query = "SELECT username, password FROM users WHERE username = ?"
        conn = sqlite3.connect(self.data_path)
        cursor = conn.cursor()
        cursor.execute(query, (u,))
        result = cursor.fetchone()
        conn.close()
        if result and self.verify_password(password, result[1]):
            if "$" not in result[1]:
                self._upgrade_password(result[0], password)
            return True
        return False

    def check_name(self, name: str):
        if len(name) < 3 or len(name) > 30:
            return False
        if (not name.isalnum()):
            return False
        if (name[0].isdigit()):
            return False
        return True

    def validate_name(self, username):
        if not self.check_name(username): return False
        conn = sqlite3.connect(self.data_path)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return False
        return True


    def validate_mail(self, email: str):
        if len(email) < 10:
            return False
        if (email.count("@") != 1):
            return False
        name, domain = email.split("@")
        if not self.check_name(name): return False
        if domain.count(".") < 1:
            return False
        components = domain.split(".")
        if self.TLDS.count(components[-1].upper()) == 0:
            return False
        conn = sqlite3.connect(self.data_path)
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return False
        return True

    def add_data(self, username: str, wpm: float, accuracy: float):
        self.check_file()
        u = username.lower()
        data = self.load_data()
        data[u] = data.get(u, {"wpm": [], "accuracy": []})
        data[u]["wpm"].append(wpm)
        data[u]["accuracy"].append(accuracy)
        with open(self.user_data_path, "w") as fs:
            json.dump(data, fs, indent=4)

    def get_data(self, username: str):
        self.check_file()
        u = username.lower()
        data = self.load_data()
        return data.get(u, {"wpm": [], "accuracy": []})

    def check_file(self):
        try:
            fs = open(self.user_data_path, "x")
            fs.close()
        except:
            pass

    def load_data(self):
        self.check_file()
        with open(self.user_data_path, "r") as fs:
            try:
                data = json.load(fs)
            except:
                data = {}
        return data
