import streamlit as st
import requests
import json

# 页面标题
st.title("🤖 Your Travel Agent")

# 初始化会话状态
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = ""

# 用户输入表单
with st.form("dify_form"):
    user_input = st.text_area("请输入您的问题：", height=150)
    submit_button = st.form_submit_button("提交")

def display_stream_response(response):
    """显示后端返回的已处理流式响应"""
    message_placeholder = st.empty()
    full_response = ""
    
    for line in response.iter_lines():
        if line.startswith(b'data:'):
            try:
                data = json.loads(line[5:])
                if 'text' in data:
                    full_response += data['text']
                    message_placeholder.markdown(full_response)
                elif 'event' in data and data['event'] == 'end':
                    break
                elif 'error' in data:
                    st.error(f"错误: {data['error']}")
            except json.JSONDecodeError:
                continue

# 处理提交
if submit_button and user_input:
    with st.spinner("正在获取回答..."):
        try:
            response = requests.post(
                "http://localhost:5000/ask",
                json={
                    "text": user_input,
                },
                stream=True
            )
            response.raise_for_status()
            
            st.success("Your Travel Agent 回答：")
            print(response.text) 
            display_stream_response(response)
        
        except requests.exceptions.RequestException as e:
            st.error(f"请求失败: {str(e)}")
        except Exception as e:
            st.error(f"发生错误: {str(e)}")