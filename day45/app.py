import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt

app = Flask(__name__)
app.secret_key = "day45-secret-key"

DB = "learning.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            day INTEGER NOT NULL,
            content TEXT NOT NULL,
            score INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hashed))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            error = "このユーザー名はすでに使われています"
    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode(), user[1]):
            session["user_id"] = user[0]
            session["username"] = username
            return redirect(url_for("dashboard"))
        error = "ユーザー名またはパスワードが違います"
    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, day, content, score, created_at FROM records WHERE user_id = ? ORDER BY day",
              (session["user_id"],))
    records = c.fetchall()
    conn.close()
    total = len(records)
    avg = round(sum(r[3] for r in records) / total, 1) if total > 0 else 0
    return render_template("dashboard.html",
                           username=session["username"],
                           records=records,
                           total=total,
                           avg=avg)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        day = request.form["day"]
        content = request.form["content"]
        score = request.form["score"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO records (user_id, day, content, score) VALUES (?, ?, ?, ?)",
                  (session["user_id"], day, content, score))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    return render_template("add.html")

@app.route("/delete/<int:record_id>")
def delete(record_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE id = ? AND user_id = ?",
              (record_id, session["user_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
