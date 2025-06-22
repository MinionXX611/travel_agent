from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DIFY_API_URL = "https://api.dify.ai/v1/workflows/run"
DIFY_API_KEY = "app-0waNF0tlWwXvhwpaAUPPx7lH"

# 你的原始Dify调用函数
@app.route("/ask", methods=["POST"])
def ask_dify():
    data = request.json
    user_input = data.get("text", "")
    
    # 原Dify调用逻辑
    inputs = {"customer_request": user_input}
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": inputs,
        "response_mode": "blocking",
        "user": "default-user"  # 可按需修改
    }

    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)