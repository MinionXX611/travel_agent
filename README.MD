# Travel Agent Chat Application - README

## 🌟 项目概述

这是一个基于Dify API的旅行代理人聊天应用，提供智能旅行建议和问答服务。前端使用Streamlit构建，后端使用Flask处理API请求。

## 🛠️ 功能特性



## 📦 技术栈

- **前端**: Streamlit
- **后端**: Flask
- **AI服务**: Dify API

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

5. **启动后端服务** (在新终端中):
   ```powershell
   python backend.py
   ```

6. **启动前端应用** (在新终端中):
   ```powershell
   streamlit run frontend.py
   ```

### macOS/Linux 环境

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 在一个终端运行
python backend.py

# 在另一个终端运行
streamlit run frontend.py
```
---

> 注意：使用时请遵守相关服务条款。