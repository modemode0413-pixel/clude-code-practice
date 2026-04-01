import os
import sqlite3
from flask import Flask, render_template, request, jsonify
import anthropic

app = Flask(__name__)

# データベースファイル名
DB = "chat_history.db"

# AnthropicクライアントをAPIキーで初期化
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def get_db():
    """DBに接続してRowオブジェクトで返す"""
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """chatsテーブルを作成する（なければ）"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                role      TEXT NOT NULL,
                message   TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


# アプリ起動時にDBを初期化
init_db()


@app.route("/")
def index():
    """トップページ：過去の会話を最大20件取得して表示"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT role, message, timestamp FROM chats ORDER BY id DESC LIMIT 20"
        ).fetchall()
    # 古い順に並べ直してHTMLに渡す
    history = list(reversed(rows))
    return render_template("index.html", history=history)


@app.route("/chat", methods=["POST"])
def chat():
    """ユーザーのメッセージをClaudeに送り、返答をDBに保存する"""
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "メッセージが空です"}), 400

    # ユーザーのメッセージをDBに保存
    with get_db() as conn:
        conn.execute(
            "INSERT INTO chats (role, message) VALUES (?, ?)",
            ("user", user_message)
        )
        conn.commit()

    # Claude APIにメッセージを送信
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.content[0].text

    # Claudeの返答をDBに保存
    with get_db() as conn:
        conn.execute(
            "INSERT INTO chats (role, message) VALUES (?, ?)",
            ("claude", reply)
        )
        conn.commit()

    return jsonify({"reply": reply})


@app.route("/clear", methods=["POST"])
def clear():
    """会話履歴を全件削除する"""
    with get_db() as conn:
        conn.execute("DELETE FROM chats")
        conn.commit()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
