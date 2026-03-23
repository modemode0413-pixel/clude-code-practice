from flask import Flask, Response
import sqlite3
import os
import json

app = Flask(__name__)

def json_response(data):
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type='application/json; charset=utf-8'
    )

DB_PATH = os.path.join(os.path.dirname(__file__), "../day27/learning.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 全学習記録を取得
@app.route('/api/records', methods=['GET'])
def get_records():
    conn = get_db()
    records = conn.execute('SELECT * FROM learning_records ORDER BY day').fetchall()
    conn.close()
    return json_response([dict(r) for r in records])

# 特定のDayの記録を取得
@app.route('/api/records/<int:day>', methods=['GET'])
def get_record(day):
    conn = get_db()
    record = conn.execute('SELECT * FROM learning_records WHERE day = ?', (day,)).fetchone()
    conn.close()
    if record is None:
        return json_response({"error": f"Day{day}のデータが見つかりません"})
    return json_response(dict(record))

# 統計情報を取得
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    stats = conn.execute('''
        SELECT
            COUNT(*) as 合計Day数,
            ROUND(AVG(score), 1) as 平均スコア,
            MAX(score) as 最高スコア,
            MIN(score) as 最低スコア
        FROM learning_records
    ''').fetchone()
    conn.close()
    return json_response(dict(stats))

if __name__ == '__main__':
    print("APIサーバー起動中...")
    print("http://localhost:5001 でアクセスできます")
    app.run(debug=True, port=5001)
