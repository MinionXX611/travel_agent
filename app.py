import streamlit as st
import requests
import json

# 设置页面配置
st.set_page_config(
    page_title="Your Travel Agent",
    page_icon="🤖",
    layout="wide"
)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏设置
with st.sidebar:
    st.title("设置")
    st.markdown("### 旅行代理人")
    st.markdown("这是一个基于Dify的旅行代理人应用。您可以在这里询问旅行相关的问题。")
    clear_button = st.button("清空对话历史")

# 清空对话历史
if clear_button:
    st.session_state.messages = []
    st.rerun()

# 页面标题
st.title("🤖 Your Travel Agent")

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def display_stream_response(response):
    """显示后端返回的已处理流式响应，并返回完整回复内容"""
    full_response = ""
    
    for line in response.iter_lines():
        if line:
            if line.startswith(b'data:'):
                try:
                    data = json.loads(line[5:])
                    if 'text' in data:
                        full_response += data['text']
                        message_placeholder.markdown(full_response + "▌")  # 添加光标效果
                    elif 'event' in data and data['event'] == 'end':
                        message_placeholder.markdown(full_response)
                        return full_response
                    elif 'error' in data:
                        st.error(f"错误: {data['error']}")
                        return None
                except json.JSONDecodeError:
                    continue
    return full_response

# 用户输入
if prompt := st.chat_input("输入消息..."):
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
                json={"text": prompt},
                stream=True
            )
            response.raise_for_status()
            
            # 处理流式响应并获取完整回复
            full_response = display_stream_response(response)
            
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