import os
from flask import Flask
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

app = Flask(__name__)

# 環境変数から設定を読み込む
APP_NAME = os.environ.get("APP_NAME", "デフォルトアプリ")
SECRET_KEY = os.environ.get("SECRET_KEY", "未設定")
ADMIN_NAME = os.environ.get("ADMIN_NAME", "名無し")
MY_MESSAGE = os.environ.get("MY_MESSAGE", "メッセージなし")

@app.route("/")
def index():
    return f"""
    <h1>{APP_NAME}</h1>
    <p>管理者: {ADMIN_NAME}</p>
    <p>秘密キー: {SECRET_KEY[:3]}***（一部のみ表示）</p>
    <p>PORT: {os.environ.get('PORT', '5000')}</p>
    <p>メッセージ: {MY_MESSAGE}</p>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
