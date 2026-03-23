import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 設定
GMAIL_ADDRESS = "modemode0413@gmail.com"
APP_PASSWORD = "urpu snlt yexh pozf"
TO_ADDRESS = "modemode0413@gmail.com"

# メール本文
body = """
Claude Code 学習レポート
========================

Day 1  ファイルを読む     80点
Day 2  ファイルを作る     85点
Day 3  フォルダ構造       90点
Day 4  コピー管理         85点
Day 5  タスク管理         88点
Day 6  ファイル編集       92点
Day 7  Grep検索          90点
Day 8  Git基本           88点
Day 9  デバッグ           85点
Day 10 Agentツール       95点

========================
平均スコア：87.8点
最高スコア：95点（Day10）
完了日数  ：35日
========================

このメールはPythonで自動送信されました。
"""

# メール作成
msg = MIMEMultipart()
msg["From"] = GMAIL_ADDRESS
msg["To"] = TO_ADDRESS
msg["Subject"] = "【自動送信】Claude Code 学習レポート"
msg.attach(MIMEText(body, "plain", "utf-8"))

# 送信
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ADDRESS, APP_PASSWORD)
        smtp.send_message(msg)
    print("メールを送信しました！")
except Exception as e:
    print(f"エラーが発生しました：{e}")
