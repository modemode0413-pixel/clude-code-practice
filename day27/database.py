import sqlite3
import sys
sys.stdout.reconfigure(encoding='utf-8')

# データベース接続
conn = sqlite3.connect('day27/learning.db')
cursor = conn.cursor()

# テーブル作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS learning_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day INTEGER,
        content TEXT,
        score INTEGER
    )
''')

# データ挿入
records = [
    (1, 'ファイルを読む', 80),
    (2, 'ファイルを作る', 85),
    (3, 'フォルダ構造', 90),
    (4, 'コピー管理', 85),
    (5, 'タスク管理', 88),
    (6, 'ファイル編集', 92),
    (7, 'Grep検索', 90),
    (8, 'Git基本', 88),
    (9, 'デバッグ', 85),
    (10, 'Agentツール', 95),
]

cursor.executemany('INSERT INTO learning_records (day, content, score) VALUES (?, ?, ?)', records)
conn.commit()

# 全件表示
print('=' * 40)
print('学習記録データベース')
print('=' * 40)
print(f'{"Day":<6} {"内容":<20} {"スコア"}')
print('-' * 40)

cursor.execute('SELECT day, content, score FROM learning_records ORDER BY day')
for row in cursor.fetchall():
    print(f'{row[0]:<6} {row[1]:<20} {row[2]}点')

print('=' * 40)
print(f'合計：{cursor.execute("SELECT COUNT(*) FROM learning_records").fetchone()[0]}件')

conn.close()
