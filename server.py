from flask import Flask, request, jsonify, Response, stream_with_context
import requests

app = Flask(__name__)

DIFY_API_URL = "https://api.dify.ai/v1/workflows/run"
DIFY_API_KEY = "app-0waNF0tlWwXvhwpaAUPPx7lH"

@app.route("/ask", methods=["POST"])
def ask_dify():
    data = request.json
    user_input = data.get("text", "")
    
    inputs = {"customer_request": user_input}
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": inputs,
        "response_mode": "streaming",
        "user": "default-user"  # 可按需修改
    }

    try:
        # 启用流式请求
        dify_response = requests.post(
            DIFY_API_URL,
            headers=headers,
            json=payload,
            stream=True  # 关键：保持流式连接
        )
        dify_response.raise_for_status()

        # 将Dify的流式响应原样转发给客户端
        return Response(
            stream_with_context(dify_response.iter_content(chunk_size=None)),
            content_type="text/event-stream"  # 保持SSE格式
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)