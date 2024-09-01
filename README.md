# coze2openai



### 安装说明

1. 确保你的系统已安装 Python 3.7 或更高版本。

2. 创建一个新的项目目录，并在其中创建一个虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 在项目根目录创建一个 `.env` 文件，包含以下内容：

```
COZE_API_KEY=你的_Coze_API_密钥
COZE_BOT_ID=你的_Coze_Bot_ID
COZE_USER_ID=你的_Coze_用户_ID
```

确保用你的实际 Coze API 凭证替换上述占位符。


### 使用说明

1. 启动服务器：

```bash
python main.py
```

这将在 `http://0.0.0.0:8000` 启动 FastAPI 服务器。

2. 使用 API：

服务器提供了一个 POST 端点 `/chat/completions`，你可以向其发送聊天请求。

示例请求：

```bash
curl -X POST http://localhost:8000/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"messages": [{"role": "user", "content": "你好，请介绍一下你自己。"}]}'
```

3. 对话管理：

- 如果你想要维护对话上下文，可以在请求头中包含 `X-Task-Id`。
- 服务器会为每个唯一的 `X-Task-Id` 创建一个新的对话，并在后续请求中保持这个对话的上下文。

示例：

```bash
curl -X POST http://localhost:8000/chat/completions \
     -H "Content-Type: application/json" \
     -H "X-Task-Id: unique-task-id-123" \
     -d '{"messages": [{"role": "user", "content": "你好，请介绍一下你自己。"}]}'
```

4. 响应：

服务器将以流式方式返回 AI 的响应。你可以实时处理这些响应块。

注意：确保你的环境变量（COZE_API_KEY、COZE_BOT_ID、COZE_USER_ID）已正确设置，否则 API 调用将失败。
