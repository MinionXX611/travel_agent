from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

DIFY_API_URL = "https://api.dify.ai/v1/workflows/run"
DIFY_API_KEY = "app-0waNF0tlWwXvhwpaAUPPx7lH"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_dify():
    # 1. 获取用户数据
    user_data = request.json
    user_input = user_data.get("query", "")
    #user_id = user_data.get("user", "default-user")  # 必填字段
    #user_input = "今天猫猫心情怎么样？"
    user_id = "default-user"  

    # 2. 构造 inputs
    inputs = {}
    inputs["customer_request"] = user_input  


    # 3. 调用 Dify Workflow
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": inputs,
        "response_mode": "blocking",  # 或 "blocking"
        "user": user_id  # 必填字段
    }

    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        print(response.json()["data"]["outputs"]["message"])
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500   

if __name__ == "__main__":
    app.run(debug=True)

"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask_dify():
    return jsonify({"status": "success"})

if __name__ == "__main__":
    print("已注册路由:", app.url_map)  # 打印路由表
    app.run(debug=True)
"""