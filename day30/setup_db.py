import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "learning.db")

# 学習データ（Day1〜29）
data = [
    (1,  "ファイルを読む",           80),
    (2,  "ファイルを作る",           80),
    (3,  "フォルダ構造",             90),
    (4,  "コピー管理",               85),
    (5,  "タスク管理",               88),
    (6,  "ファイル編集",             92),
    (7,  "Grep検索",                90),
    (8,  "Git基本",                  88),
    (9,  "デバッグ",                 85),
    (10, "Agentツール",              95),
    (11, "Webブラウザ操作",          88),
    (12, "プロジェクト設計と実装",    90),
    (13, "コードレビュー",           87),
    (14, "Week2総復習",              92),
    (15, "自動化スクリプト",          90),
    (16, "複数ファイル一括処理",      88),
    (17, "テンプレート作成",          91),
    (18, "自動レポート生成",          93),
    (19, "GitHub連携",               89),
    (20, "HTML/CSS作成",             90),
    (21, "Pythonスクリプト",         92),
    (23, "データ分析CSV",            91),
    (24, "自動レポート発展版",        93),
    (25, "Gitブランチ・マージ",       90),
    (26, "Webスクレイピング",         88),
    (27, "SQLiteデータベース",        92),
    (28, "FlaskWebアプリ",           94),
    (29, "JSON処理・設定ファイル",    91),
]

# データベース作成
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS learning")
c.execute("""
    CREATE TABLE learning (
        day     INTEGER PRIMARY KEY,
        content TEXT NOT NULL,
        score   INTEGER NOT NULL
    )
""")

c.executemany("INSERT INTO learning VALUES (?, ?, ?)", data)
conn.commit()
conn.close()

print(f"データベース作成完了！")
print(f"登録件数：{len(data)}件")
print(f"保存先：{db_path}")
