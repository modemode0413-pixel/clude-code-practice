from flask import Flask, Response
import json

app = Flask(__name__)

learning_data = [
    {"day": 1, "content": "ファイルを読む", "score": 80},
    {"day": 2, "content": "ファイルを作る", "score": 85},
    {"day": 3, "content": "フォルダ構造", "score": 90},
    {"day": 4, "content": "コピー管理", "score": 85},
    {"day": 5, "content": "タスク管理", "score": 88},
    {"day": 6, "content": "ファイル編集", "score": 92},
    {"day": 7, "content": "Grep検索", "score": 90},
    {"day": 8, "content": "Git基本", "score": 88},
    {"day": 9, "content": "デバッグ", "score": 85},
    {"day": 10, "content": "Agentツール", "score": 95},
]

@app.route('/')
def index():
    avg = sum(d["score"] for d in learning_data) / len(learning_data)
    best = max(learning_data, key=lambda x: x["score"])

    rows = ""
    for d in learning_data:
        rows += f"<tr><td>Day {d['day']}</td><td>{d['content']}</td><td>{d['score']}点</td></tr>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Claude Code 学習記録</title>
        <style>
            body {{ font-family: sans-serif; max-width: 700px; margin: 40px auto; background: #f5f5f5; }}
            h1 {{ text-align: center; color: #333; }}
            .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
            .stat {{ flex: 1; background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stat h3 {{ color: #666; font-size: 14px; margin: 0 0 8px; }}
            .stat p {{ color: #333; font-size: 28px; font-weight: bold; margin: 0; }}
            table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            th {{ background: #333; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 12px; border-bottom: 1px solid #eee; }}
            .badge {{ background: #007bff; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <h1>🎓 Claude Code 学習記録</h1>
        <div class="stats">
            <div class="stat"><h3>完了Day</h3><p>{len(learning_data)}日</p></div>
            <div class="stat"><h3>平均スコア</h3><p>{avg:.1f}点</p></div>
            <div class="stat"><h3>最高スコア</h3><p>{best['score']}点</p></div>
        </div>
        <table>
            <tr><th>Day</th><th>内容</th><th>スコア</th></tr>
            {rows}
        </table>
        <p style="text-align:center; color:#999; margin-top:20px;">🐳 Dockerコンテナで動作中</p>
    </body>
    </html>
    """
    return Response(html, content_type='text/html; charset=utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
