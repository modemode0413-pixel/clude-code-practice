import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import bcrypt

app = Flask(__name__)
app.secret_key = "day45-secret-key"

DB = "learning.db"

def get_db():
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect(DB, timeout=10) as conn:
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
            with get_db() as conn:
                c = conn.cursor()
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                          (username, hashed))
                conn.commit()
            flash("✅ 登録しました。ログインしてください", "success")
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
        with get_db() as conn:
            c = conn.cursor()
            c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = c.fetchone()
        if user and bcrypt.checkpw(password.encode(), user[1]):
            session["user_id"] = user[0]
            session["username"] = username
            return redirect(url_for("dashboard"))
        error = "ユーザー名またはパスワードが違います"
    return render_template("login.html", error=error)

PER_PAGE = 5

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    keyword = request.args.get("keyword", "")
    page = max(1, int(request.args.get("page", 1)))
    with get_db() as conn:
        c = conn.cursor()
        if keyword:
            c.execute("SELECT COUNT(*) FROM records WHERE user_id = ? AND content LIKE ?",
                      (session["user_id"], f"%{keyword}%"))
        else:
            c.execute("SELECT COUNT(*) FROM records WHERE user_id = ?",
                      (session["user_id"],))
        total = c.fetchone()[0]
        if keyword:
            c.execute("SELECT id, day, content, score, created_at FROM records WHERE user_id = ? AND content LIKE ? ORDER BY day LIMIT ? OFFSET ?",
                      (session["user_id"], f"%{keyword}%", PER_PAGE, (page - 1) * PER_PAGE))
        else:
            c.execute("SELECT id, day, content, score, created_at FROM records WHERE user_id = ? ORDER BY day LIMIT ? OFFSET ?",
                      (session["user_id"], PER_PAGE, (page - 1) * PER_PAGE))
        records = c.fetchall()
        if keyword:
            c.execute("SELECT score FROM records WHERE user_id = ? AND content LIKE ?",
                      (session["user_id"], f"%{keyword}%"))
        else:
            c.execute("SELECT score FROM records WHERE user_id = ?",
                      (session["user_id"],))
        all_scores = [r[0] for r in c.fetchall()]
    avg = round(sum(all_scores) / total, 1) if total > 0 else 0
    total_pages = (total + PER_PAGE - 1) // PER_PAGE
    return render_template("dashboard.html",
                           username=session["username"],
                           records=records,
                           total=total,
                           avg=avg,
                           keyword=keyword,
                           page=page,
                           total_pages=total_pages)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        day = request.form["day"]
        content = request.form["content"]
        score = request.form["score"]
        with get_db() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO records (user_id, day, content, score) VALUES (?, ?, ?, ?)",
                      (session["user_id"], day, content, score))
            conn.commit()
        flash("✅ 記録を保存しました", "success")
        return redirect(url_for("dashboard"))
    return render_template("add.html")

@app.route("/edit/<int:record_id>", methods=["GET", "POST"])
def edit(record_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        day = request.form["day"]
        content = request.form["content"]
        score = request.form["score"]
        with get_db() as conn:
            c = conn.cursor()
            c.execute("UPDATE records SET day = ?, content = ?, score = ? WHERE id = ? AND user_id = ?",
                      (day, content, score, record_id, session["user_id"]))
            conn.commit()
        flash("✅ 記録を更新しました", "success")
        return redirect(url_for("dashboard"))
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT id, day, content, score FROM records WHERE id = ? AND user_id = ?",
                  (record_id, session["user_id"]))
        record = c.fetchone()
    return render_template("edit.html", record=record)

@app.route("/delete/<int:record_id>")
def delete(record_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    with get_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM records WHERE id = ? AND user_id = ?",
                  (record_id, session["user_id"]))
        conn.commit()
    flash("🗑 記録を削除しました", "info")
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    flash("👋 ログアウトしました", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
