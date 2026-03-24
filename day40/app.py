import sqlite3
import os
from flask import Flask

app = Flask(__name__)

# デプロイ用：学習データをコードに直接埋め込む
LEARNING_DATA = [
    (1, "ファイルを読む", 80),
    (2, "ファイルを作る", 85),
    (3, "フォルダ構造", 90),
    (4, "コピー管理", 85),
    (5, "タスク管理", 88),
    (6, "ファイル編集", 92),
    (7, "Grep検索", 90),
    (8, "Git基本", 88),
    (9, "デバッグ", 85),
    (10, "Agentツール", 95),
    (11, "Web検索", 88),
    (12, "プロジェクト設計", 90),
    (13, "コードレビュー", 92),
    (14, "Week2総復習", 88),
    (15, "自動化スクリプト", 90),
    (16, "一括処理", 85),
    (17, "テンプレート", 88),
    (18, "自動レポート", 90),
    (19, "GitHub連携", 85),
    (20, "HTML/CSS", 92),
    (21, "Python入門", 88),
    (22, "データ分析", 90),
    (23, "データ分析CSV", 92),
    (24, "自動レポート発展", 88),
    (25, "Gitブランチ", 90),
    (26, "Webスクレイピング", 88),
    (27, "SQLite", 92),
    (28, "Flask Webアプリ", 90),
    (29, "JSON設定ファイル", 88),
    (30, "総仕上げ", 95),
]


@app.route("/")
def index():
    rows = LEARNING_DATA
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
