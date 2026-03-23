import sqlite3
from flask import Flask

app = Flask(__name__)

def get_records():
    conn = sqlite3.connect('day27/learning.db')
    cursor = conn.cursor()
    cursor.execute('SELECT day, content, score FROM learning_records ORDER BY day')
    records = cursor.fetchall()
    cursor.execute('SELECT AVG(score), MAX(score), MIN(score) FROM learning_records')
    avg, max_s, min_s = cursor.fetchone()
    conn.close()
    return records, avg, max_s, min_s

@app.route('/')
def index():
    records, avg, max_s, min_s = get_records()

    rows = ''
    for day, content, score in records:
        color = '#4CAF50' if score >= 90 else '#2196F3' if score >= 85 else '#FF9800'
        rows += f'''
        <tr>
            <td>Day {day}</td>
            <td>{content}</td>
            <td style="color:{color}; font-weight:bold;">{score}点</td>
        </tr>'''

    html = f'''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>Claude Code 学習記録</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; background: #f5f5f5; }}
            h1 {{ color: #333; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            th {{ background: #333; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
            tr:last-child td {{ border-bottom: none; }}
            .stats {{ display: flex; gap: 16px; margin-top: 20px; }}
            .stat {{ flex: 1; background: white; padding: 16px; border-radius: 8px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .stat h3 {{ margin: 0 0 8px; color: #666; font-size: 14px; }}
            .stat p {{ margin: 0; font-size: 24px; font-weight: bold; color: #333; }}
        </style>
    </head>
    <body>
        <h1>Claude Code 学習記録</h1>
        <table>
            <tr><th>Day</th><th>内容</th><th>スコア</th></tr>
            {rows}
        </table>
        <div class="stats">
            <div class="stat"><h3>平均スコア</h3><p>{avg:.1f}点</p></div>
            <div class="stat"><h3>最高スコア</h3><p>{max_s}点</p></div>
            <div class="stat"><h3>最低スコア</h3><p>{min_s}点</p></div>
        </div>
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    app.run(debug=True)
