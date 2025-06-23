import streamlit as st
import requests
import json
import html2text

# 页面标题
st.title("🤖 Your Travel Agent")

# 用户输入表单
with st.form("dify_form"):
    user_input = st.text_area("请输入您的问题：", height=150)
    submit_button = st.form_submit_button("提交")

# 处理流式输出
def stream_response(response):
    buffer = ""
    should_output = False  # 标记是否开始输出
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.single_line_break = True
    converter.wrap_links = False
    
    for chunk in response.iter_content(chunk_size=None):
        buffer += chunk.decode('utf-8')
        
        while "\n\n" in buffer:
            line, buffer = buffer.split("\n\n", 1)
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith(':'):
                continue
                
            if line.startswith("data: "):
                json_str = line[6:].strip()
                if not json_str:  # 空数据
                    continue
                    
                try:
                    event_data = json.loads(json_str)
                    if event_data.get("event") == "text_chunk":
                        text = event_data["data"]["text"]
                        
                        # 检查是否包含</details>标签
                        if not should_output:
                            if "</details>" in text:
                                should_output = True
                                # 只输出</details>之后的内容
                                text = text.split("</details>")[-1].strip()
                                if text:  # 确保分割后不是空字符串
                                    cleaned_text = converter.handle(text)
                                    cleaned_text = ''.join(cleaned_text.split())
                                    yield cleaned_text
                            continue
                        
                        # 如果已经检测到</details>，正常输出
                        cleaned_text = converter.handle(text)
                        cleaned_text = ''.join(cleaned_text.split())
                        yield cleaned_text
                        
                    elif event_data.get("event") == "workflow_finished":
                        return
                        
                except json.JSONDecodeError as e:
                    st.warning(f"解析 JSON 失败: {e}\n原始数据: {json_str}")
                    continue
                except KeyError as e:
                    st.warning(f"缺少预期字段: {e}\n数据: {event_data}")
                    continue

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
            st.success("Your Travel Agent 回答：")
            st.write_stream(stream_response(response))
        
        except Exception as e:
            st.error(f"详细错误: {type(e)} - {str(e)}")


            