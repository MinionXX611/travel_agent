import streamlit as st
import requests

# 页面标题
st.title("🤖 Your Travel Agent")

# 用户输入表单
with st.form("dify_form"):
    user_input = st.text_area("请输入您的问题：", height=150)
    submit_button = st.form_submit_button("提交")

# 处理提交
if submit_button and user_input:
    with st.spinner("正在获取回答..."):
        try:
            # 调用后端API
            response = requests.post(
                "http://localhost:5000/ask",  # 指向你的Flask后端
                json={"text": user_input}
            )
            response.raise_for_status()
            
            # 显示结果
            result = response.json()
            st.success("Dify 回答：")
            st.write(result["data"]["outputs"]["message"])
            
        except Exception as e:
            st.error(f"请求失败: {str(e)}")