import sqlite3
import os
from flask import Flask

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "learning.db")


def get_data():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT day, content, score FROM learning ORDER BY day")
    rows = c.fetchall()
    conn.close()
    return rows


@app.route("/")
def index():
    rows = get_data()
    total = len(rows)
    avg = round(sum(r[2] for r in rows) / total, 1) if total > 0 else 0
    best = max(rows, key=lambda r: r[2])

    rows_html = ""
    for day, content, score in rows:
        color = "#4CAF50" if score >= 90 else "#2196F3"
        rows_html += f"""
        <tr>
            <td>Day {day}</td>
            <td>{content}</td>
            <td style="color:{color}; font-weight:bold;">{score}点</td>
        </tr>"""

    html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>じゅんのClaude Code学習記録</title>
        <style>
            body {{ font-family: sans-serif; max-width: 800px; margin: 40px auto; background: #f5f5f5; }}
            h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
            .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
            .stat-box {{ background: white; padding: 20px; border-radius: 8px; flex: 1; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stat-box h2 {{ font-size: 2em; margin: 0; color: #4CAF50; }}
            .stat-box p {{ margin: 5px 0 0; color: #666; }}
            table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
            tr:hover {{ background: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>🎓 じゅんの Claude Code 学習記録</h1>
        <div class="stats">
            <div class="stat-box">
                <h2>{total}日</h2>
                <p>📅 完了したDay</p>
            </div>
            <div class="stat-box">
                <h2>{avg}点</h2>
                <p>⭐ 平均スコア</p>
            </div>
            <div class="stat-box">
                <h2>{best[2]}点</h2>
                <p>🏆 最高スコア（Day{best[0]}）</p>
            </div>
        </div>
        <table>
            <tr><th>Day</th><th>内容</th><th>スコア</th></tr>
            {rows_html}
        </table>
    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    app.run(debug=True)
