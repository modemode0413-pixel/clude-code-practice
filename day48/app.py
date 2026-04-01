import os
from flask import Flask, render_template, request, jsonify
import anthropic

app = Flask(__name__)

# AnthropicクライアントをAPIキーで初期化
# APIキーは環境変数 ANTHROPIC_API_KEY から読み込む
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "メッセージが空です"}), 400

    # Claude APIにメッセージを送信
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    # レスポンスからテキストを取り出す
    reply = response.content[0].text
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
