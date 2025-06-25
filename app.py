import streamlit as st
import requests
import json
from schemas.chat import ASK_REQUEST_SCHEMA
from jsonschema import validate, ValidationError
from utils.security import filter_util
import time

# 设置页面配置
st.set_page_config(
    page_title="Your Travel Agent",
    page_icon="🤖",
    layout="wide"
)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 添加初始欢迎消息
    st.session_state.messages.append({
        "role": "assistant",
        "content": "你好，我是你的专属旅行规划师，请告诉我您的旅行时间、人数、出发地、旅行地、预算、旅行偏好，我将为您生成详细的旅行计划"
    })
    
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ''

# 侧边栏设置
with st.sidebar:
    st.title("设置")
    st.markdown("### 旅行代理人")
    st.markdown("这是一个基于Dify的旅行代理人应用。您可以在这里询问旅行相关的问题。")
    clear_button = st.button("清空对话历史")

# 清空对话历史
if clear_button:
    st.session_state.messages = []
    st.session_state.conversation_id = '' 
    st.rerun()

# 页面标题
st.title("🤖 Your Travel Agent")

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def validate_input(text):
    """验证用户输入"""
    try:
        validate(instance=text, schema=ASK_REQUEST_SCHEMA["properties"]["text"])
        has_sensitive, _ = filter_util.filter(text)
        if has_sensitive:
            return False, "输入包含不允许的内容"
        return True, None
    except ValidationError as e:
        return False, f"输入无效: {e.message}"

def display_stream_response(response):
    """显示后端返回的已处理流式响应，并返回完整回复内容和conversation_id"""
    full_response = ""
    conversation_id = ''
    buffer = ""
    last_update_time = 0
    update_interval = 0.1  # 更新间隔(秒)
    current_time = time.time()
    
    for line in response.iter_lines():
        if line:
            if line.startswith(b'data:'):
                try:
                    data = json.loads(line[5:])
                    if 'text' in data:
                        buffer += data['text']
                        full_response += data['text']
                        
                        # 控制更新频率，避免过于频繁的DOM操作
                        current_time = time.time()
                        if current_time - last_update_time > update_interval or len(buffer) > 50:
                            message_placeholder.markdown(full_response + "▌")
                            buffer = ""
                            last_update_time = current_time
                            
                    elif 'conversation_id' in data:
                        conversation_id = data['conversation_id']
                    elif 'event' in data and data['event'] == 'end':
                        # 确保最终显示完整内容
                        message_placeholder.markdown(full_response)
                        return full_response, conversation_id
                    elif 'error' in data:
                        st.error(f"错误: {data['error']}")
                        return None, None
                except json.JSONDecodeError as e:
                    st.warning(f"数据解析异常: {str(e)}")
                    continue
    
    # 最终确保显示完整内容
    if full_response:
        message_placeholder.markdown(full_response)
    return full_response, conversation_id

# 用户输入
if prompt := st.chat_input("输入消息..."):
    is_valid, error_msg = validate_input(prompt)
    if not is_valid:
        st.error(error_msg)
        st.stop()  # 停止执行当前运行
    
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 显示AI回复占位符
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("思考中...")
        
        try:
            response = requests.post(
                "http://localhost:5000/ask",
                json={
                    "text": prompt,
                    "conversation_id": st.session_state.conversation_id  # 传递当前会话ID
                },
                stream=True
            )
            response.raise_for_status()
            
            # 处理流式响应并获取完整回复和conversation_id
            full_response, new_conversation_id = display_stream_response(response)
            
            if new_conversation_id:
                st.session_state.conversation_id = new_conversation_id
            
            if full_response:
                # 只有成功获取完整回复后才添加到历史记录
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            
        except requests.exceptions.Timeout:
            st.error("请求超时，请稍后再试")
        except requests.exceptions.ConnectionError:
            st.error("无法连接到服务器，请检查网络")
        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {str(e)}")
        except Exception as e:
            st.error(f"发生意外错误: {str(e)}")