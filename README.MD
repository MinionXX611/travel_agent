# Travel Agent Chat Application - README

## 🌟 项目概述

这是一个基于Dify API的旅行代理人聊天应用，提供智能旅行建议和问答服务。前端使用Streamlit构建，后端使用Flask处理API请求。

## 🛠️ 功能特性

**✨ 核心功能：**  
1. **个性化行程定制**  
   - 只需告知旅行时间、人数、预算和偏好，AI即刻生成完整行程  
   - 智能推荐景点/餐厅/交通方案，匹配您的兴趣标签  

2. **实时交互优化**  
   - 像朋友一样自然对话："我想看海但怕人多""预算增加2k怎么调整？"  
   - 支持随时修改需求，行程动态更新  

3. **全流程贴心服务**  
   - 从签证须知到当地天气提醒  
   - 内置智能预算分配器，费用明细一目了然  

**🌍 为什么选择我们？**  
- 3秒响应速度，告别传统攻略查阅  
- 覆盖全球10万+目的地数据  
- 隐私保护：您的行程数据仅您可见  

*"告诉我去哪、和谁、花多少，剩下的交给我"*  

（小提示：尝试说"5月带父母去京都，3天2晚预算1.5万，要温泉和轮椅通道"体验完整服务）


## 📦 技术栈

- **前端**: Streamlit
- **后端**: Flask
- **AI服务**: Dify API

我已经为您在部署方案中添加了设置`.env`文件的环节。以下是更新后的README内容：

## 🚀 部署与运行

### Windows 环境

1. **创建虚拟环境**:
   ```powershell
   python -m venv venv
   ```

2. **设置执行策略** (仅首次需要):
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. **激活虚拟环境**:
   ```powershell
   .\venv\Scripts\activate
   ```

4. **安装依赖**:
   ```powershell
   pip install -r requirements.txt
   ```

5. **配置环境变量**:
   - 在项目根目录的`.env`文件填入我们的API密钥
     ```
     DIFY_API_KEY = "app-ANs22fGiGQdRi101fBwOl6Fb"
     ```

6. **启动后端服务** (在新终端中):
   ```powershell
   python server.py
   ```

7. **启动前端应用** (在新终端中):
   ```powershell
   streamlit run app.py
   ```

### macOS/Linux 环境

```bash
pip3 install -r requirements.txt

# 配置环境变量
echo "DIFY_API_KEY = "app-ANs22fGiGQdRi101fBwOl6Fb"" >> .env

# 在一个终端运行
python server.py

# 在另一个终端运行
streamlit run app.py
```
## 📌 输出/使用样例
📥 (./examples/输出样例.pdf)

---

> 注意：使用时请遵守相关服务条款。