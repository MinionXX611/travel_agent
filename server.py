from flask import Flask, request, Response, stream_with_context, jsonify
import requests
import json
import html2text

app = Flask(__name__)

DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = "app-RkuXkUDc9Fxsh4L9nF9Fu1qz"

def process_dify_stream(response):
    """处理Dify的流式响应并返回清洗后的文本"""
    buffer = ""
    should_output = False
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.single_line_break = True
    converter.wrap_links = False
    
    for chunk in response.iter_content(chunk_size=None):
        buffer += chunk.decode('utf-8')
        
        while "\n\n" in buffer:
            line, buffer = buffer.split("\n\n", 1)
            line = line.strip()
            
            if not line or line.startswith(':'):
                continue
                
            if line.startswith("data: "):
                json_str = line[6:].strip()
                if not json_str:
                    continue
                    
                try:
                    event_data = json.loads(json_str)
                    if event_data.get("event") == "message":
                        text = event_data["answer"]
                        conversation_id = event_data.get("conversation_id")
                        
                        # 返回conversation_id给前端
                        if conversation_id:
                            yield f"data: {json.dumps({'conversation_id': conversation_id})}\n\n"
                        
                        # 处理</details>标签
                        if not should_output and "</details>" in text:
                            should_output = True
                            text = text.split("</details>")[-1].strip()
                        
                        if should_output and text:
                            cleaned_text = converter.handle(text)
                            cleaned_text = ''.join(cleaned_text.split())
                            yield f"data: {json.dumps({'text': cleaned_text})}\n\n"
                    elif event_data.get("event") == "message_end":
                        yield "data: {\"event\": \"end\"}\n\n"
                        return
                        
                except (json.JSONDecodeError, KeyError) as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.route("/ask", methods=["POST"])
def ask_dify():
    data = request.json
    user_input = data.get("text", "")
    conversation_id = data.get("conversation_id")  # 从前端获取当前会话ID
    
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": user_input,
        "response_mode": "streaming",
        "conversation_id": conversation_id,  # 传递给Dify API
        "user": "travel_user"
    }

    try:
        dify_response = requests.post(
            DIFY_API_URL,
            headers=headers,
            json=payload,
            stream=True
        )
        dify_response.raise_for_status()
        
        return Response(
            stream_with_context(process_dify_stream(dify_response)),
            content_type="text/event-stream"
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)