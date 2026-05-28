from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

API_KEY = "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"
MODEL   = "openai/gpt-oss-120b"

client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful, smart, and friendly AI assistant. "
    "Answer clearly and concisely. When writing code, always use "
    "proper formatting with comments."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data     = request.get_json()
    history  = data.get("history", [])
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": user_msg})

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=1024,
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
