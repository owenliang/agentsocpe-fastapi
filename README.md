# agentsocpe-fastapi

## 项目背景

本项目是一个基于 AgentScope 和 FastAPI 构建的聊天机器人应用。AgentScope 是阿里巴巴开源的一套多智能体开发框架，提供了构建 LLM 应用的标准化流程和工具集。该项目旨在展示如何利用 AgentScope 快速搭建一个具有流式传输能力的聊天机器人服务，并通过 FastAPI 提供 RESTful API 接口。

该应用支持实时对话功能，用户可以通过前端界面与基于大语言模型的聊天机器人进行交互。后端采用 Server-Sent Events (SSE) 技术实现流式响应，使用户能够实时看到机器人的逐步回复，提供更自然的对话体验。

![聊天机器人界面示例](chatbot.png)

## 关键技术挑战

### 1. 实时流式传输
实现从后端模型到前端界面的实时数据传输是一项关键技术挑战。传统的 HTTP 请求-响应模式无法满足实时显示生成内容的需求。

### 2. 多用户会话管理
在多用户并发访问场景下，需要有效管理每个用户的独立会话状态，确保对话上下文不会混乱。

### 3. 前后端异步通信
前端需要以非阻塞方式接收后端逐步生成的内容，并实时更新界面，这对异步处理机制提出了较高要求。

### 4. 用户体验优化
需要处理各种边界情况，如网络中断、重复请求、输入验证等，以保证良好的用户体验。

## 解决方案

### 1. SSE 流式传输技术
采用 Server-Sent Events (SSE) 实现从服务端向客户端的单向实时数据推送。相比 WebSocket 更加轻量级，适合聊天机器人这种主要是服务端向客户端推送数据的场景。

### 2. AgentScope 会话管理
利用 AgentScope 内置的会话管理机制，为每个用户维护独立的对话历史记录。通过用户名标识不同用户，确保对话上下文隔离。

### 3. FastAPI 异步支持
基于 FastAPI 的异步特性，实现高并发处理能力。使用 StreamingResponse 返回流式数据，配合 AgentScope 的生成器模式，实现端到端的异步处理。

### 4. 前端状态管理
前端通过 JavaScript 实现详细的状态管理，包括：
- 用户名输入控制
- 消息发送状态跟踪
- 实时滚动更新聊天窗口
- 错误处理和连接状态监控

### 5. 用户体验优化措施
- 实时禁用/启用输入控件防止重复提交
- 自动滚动聊天窗口确保最新消息可见
- 优雅处理连接异常和中断情况
- 支持 Enter 键快速发送消息

## 项目结构

```
agentscope-fastapi/
├── chatbot.py              # 后端主程序，基于 FastAPI 实现 SSE 流式接口
├── front.html              # 前端界面，使用 HTML/CSS/JavaScript 实现
├── clibot.py               # 命令行版本的聊天机器人
├── requirements.txt        # 项目依赖包列表
├── sessions/               # 会话数据存储目录
└── README.md              # 项目说明文档
```

## 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

1. 克隆或下载项目代码

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
需要设置 `API_KEY` 环境变量，用于访问大语言模型 API：
```bash
export API_KEY=your_api_key_here
```

4. 运行后端服务：
```bash
python chatbot.py
```

服务默认运行在 `http://localhost:8000`

5. 打开前端界面：
在浏览器中打开 [front.html](file://c:\Users\owen\Documents\VsCode\agentsocpe-fastapi\front.html) 文件，或访问 `http://localhost:8000`

## API 接口说明

### 流式聊天接口

```
GET /stream
```

该接口使用 Server-Sent Events (SSE) 技术实现实时流式传输。

**参数：**
- `username` (string, required): 用户名，用于标识不同的会话
- `query` (string, required): 用户的聊天消息

**响应：**
- Content-Type: text/event-stream
- 返回 Server-Sent Events 格式的流式数据

**示例请求：**
```bash
curl "http://localhost:8000/stream?username=Alice&query=你好"
```

**响应格式：**
```
data: {"message": "你"}
data: {"message": "你好"}
data: {"message": "你好！"}
data: {"message": "你好！有什么"}
data: {"message": "你好！有什么我可以"}
data: {"message": "你好！有什么我可以帮助"}
data: {"message": "你好！有什么我可以帮助你的"}
data: {"message": "你好！有什么我可以帮助你的吗？"}

```

每个 `data` 行代表模型生成过程中的一个片段，前端通过 SSE 实时接收并展示这些片段。

### 健康检查接口

```
GET /docs
```

FastAPI 自动生成的 API 文档界面，可以查看所有可用接口并进行测试。

## 使用说明

1. 在前端界面的用户名输入框中输入您的昵称
2. 在消息输入框中输入您想与聊天机器人交流的内容
3. 点击"发送"按钮或按回车键发送消息
4. 实时查看聊天机器人的回复

注意：当切换用户名时，聊天记录会自动清空，确保每个用户都有独立的聊天环境。

## 对话记忆

```
{
"agent":{
"memory":{
"content":[
{
"id":"PttiNSespV9yTLvHsqbH6y",
"name":"owen",
"role":"user",
"content":"你好",
"metadata":null,
"timestamp":"2025-11-02 15:27:43.849"
},
{
"id":"8JodLyTk93YeDm7McobuDx",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"id":"HmhA3UrY4RPGSTdpcMdpaV",
"type":"tool_use",
"name":"generate_response",
"input":{
"response":"你好！有什么好玩的事情要跟我分享，或者需要我帮什么忙吗？别告诉我你只是来打个招呼的，我可不信～ 😜"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:27:44.851"
},
{
"id":"oFiEiBjnsr8wWLrpiEjqNh",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"HmhA3UrY4RPGSTdpcMdpaV",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:27:47.032"
},
{
"id":"cSMSuUxoqJ5Vyx9iXCY4Y9",
"name":"ChatBot",
"role":"assistant",
"content":"你好！有什么好玩的事情要跟我分享，或者需要我帮什么忙吗？别告诉我你只是来打个招呼的，我可不信～ 😜",
"metadata":null,
"timestamp":"2025-11-02 15:27:47.032"
},
{
"id":"XyAbXEPbZNDroV3eWEkwoS",
"name":"owen",
"role":"user",
"content":"你叫什么名字",
"metadata":null,
"timestamp":"2025-11-02 15:27:54.756"
},
{
"id":"2e9uamW8ftmBo3MbqzWntK",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"id":"TSdTMtXk55WgnzvRy2XkiJ",
"type":"tool_use",
"name":"generate_response",
"input":{
"response":"哈哈，你这是在跟我玩‘猜猜我是谁’的游戏吗？不过呢，我可是一个超级有幽默感的AI助手，你可以叫我小乐。有什么好玩的事情想和小乐一起分享吗？ 😄"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:27:55.210"
},
{
"id":"D4ooQUNoYDNyeYnYPihbP4",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"TSdTMtXk55WgnzvRy2XkiJ",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:27:59.780"
},
{
"id":"NJTVCU7VFSb7Eoyd4JqDjM",
"name":"ChatBot",
"role":"assistant",
"content":"哈哈，你这是在跟我玩‘猜猜我是谁’的游戏吗？不过呢，我可是一个超级有幽默感的AI助手，你可以叫我小乐。有什么好玩的事情想和小乐一起分享吗？ 😄",
"metadata":null,
"timestamp":"2025-11-02 15:27:59.780"
},
{
"id":"SURgQ6TgUFFnYKM5DFfteX",
"name":"owen",
"role":"user",
"content":"讲个笑话",
"metadata":null,
"timestamp":"2025-11-02 15:28:09.515"
},
{
"id":"A8zp2Ds6bnfqRgTLuLmx9u",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"type":"tool_use",
"id":"call_0f01d4012b27446593a8c3",
"name":"generate_response",
"input":{
"response":"好的，那我就给你讲个笑话吧！为什么电脑经常生病？\n\n因为它的窗户（Windows）总是开着啊！哈哈～ 😂"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:28:10.808"
},
{
"id":"a8N5eWfQs3hHEmKp4FQS8F",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"call_0f01d4012b27446593a8c3",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:28:12.220"
},
{
"id":"2NPgA372La9LTPxSaszk7H",
"name":"ChatBot",
"role":"assistant",
"content":"好的，那我就给你讲个笑话吧！为什么电脑经常生病？\n\n因为它的窗户（Windows）总是开着啊！哈哈～ 😂",
"metadata":null,
"timestamp":"2025-11-02 15:28:12.220"
},
{
"id":"k3tiZBNVVtxiYaHVqK5gKi",
"name":"owen",
"role":"user",
"content":"你最后一句讲了什么",
"metadata":null,
"timestamp":"2025-11-02 15:28:39.786"
},
{
"id":"oFHLPyeRWoRaLs8YUHq6FM",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"id":"UGs2Arej4P3bNJprAKJbYF",
"type":"tool_use",
"name":"generate_response",
"input":{
"response":"我刚刚讲了一个关于电脑的笑话哦，说的是为什么电脑经常生病，答案是因为它的窗户（Windows）总是开着。这是一个小小的文字游戏，把操作系统Windows当作了真的窗户。希望这个笑话能让你会心一笑！😄 如果你没听清楚或者想要听一个新的笑话，告诉我就好了！"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:28:40.304"
},
{
"id":"oASPHW28uXFnuDtuQPjLvZ",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"UGs2Arej4P3bNJprAKJbYF",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:28:43.275"
},
{
"id":"KDjLGpvVYCiPy5T9xucFGH",
"name":"ChatBot",
"role":"assistant",
"content":"我刚刚讲了一个关于电脑的笑话哦，说的是为什么电脑经常生病，答案是因为它的窗户（Windows）总是开着。这是一个小小的文字游戏，把操作系统Windows当作了真的窗户。希望这个笑话能让你会心一笑！😄 如果你没听清楚或者想要听一个新的笑话，告诉我就好了！",
"metadata":null,
"timestamp":"2025-11-02 15:28:43.275"
},
{
"id":"fvmZSo8c4TbtuDAXXZuFHJ",
"name":"owen",
"role":"user",
"content":"你好",
"metadata":null,
"timestamp":"2025-11-02 15:30:57.611"
},
{
"id":"3SzNBuvp8YzQj8YUnzQRFy",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"id":"bEtreUkDXBawRqogBGLGWR",
"type":"tool_use",
"name":"generate_response",
"input":{
"response":"你好！我们又见面啦，有什么新鲜事儿想跟我聊聊吗？或者你想要再来点欢乐的笑话？😉"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:30:58.368"
},
{
"id":"dToUkQpkYU4DMex8Z5eCsC",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"bEtreUkDXBawRqogBGLGWR",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:31:00.195"
},
{
"id":"CswYutWhutkY8MxpRbftsj",
"name":"ChatBot",
"role":"assistant",
"content":"你好！我们又见面啦，有什么新鲜事儿想跟我聊聊吗？或者你想要再来点欢乐的笑话？😉",
"metadata":null,
"timestamp":"2025-11-02 15:31:00.195"
},
{
"id":"D8J28m7hrQHgDP9YufiEBN",
"name":"owen",
"role":"user",
"content":"呵呵",
"metadata":null,
"timestamp":"2025-11-02 15:32:00.300"
},
{
"id":"ikDZnqA8DbEaUsLtJFuLpA",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"type":"tool_use",
"id":"call_7a5263ce7ff24be8967b32",
"name":"generate_response",
"input":{
"response":"呵呵，这笑声里充满了故事啊！不过我猜你可能想要来点更有趣的？那再来个笑话如何：为什么数学书总是最不开心的？因为它总是有很多问题！😄"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:01.521"
},
{
"id":"iaCMaPGYoCuWgxmf6rNZvv",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"call_7a5263ce7ff24be8967b32",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:05.169"
},
{
"id":"2vBc9gx7pWQ85GyjAMLSif",
"name":"ChatBot",
"role":"assistant",
"content":"呵呵，这笑声里充满了故事啊！不过我猜你可能想要来点更有趣的？那再来个笑话如何：为什么数学书总是最不开心的？因为它总是有很多问题！😄",
"metadata":null,
"timestamp":"2025-11-02 15:32:05.170"
},
{
"id":"dmVZFKssuHJKH4uNRKoUC6",
"name":"owen",
"role":"user",
"content":"你刚才讲过一个windows笑话？",
"metadata":null,
"timestamp":"2025-11-02 15:32:13.404"
},
{
"id":"eaQwdwG44yzsF2bBvLzHT2",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"type":"tool_use",
"id":"call_f980d2ddcad24e8588e156",
"name":"generate_response",
"input":{
"response":"对的，那个笑话是这样的：为什么电脑经常生病？因为它的窗户（Windows）总是开着啊！这是一个利用了双关的小幽默，把电脑的操作系统Windows比作了真的窗户。希望这个笑话能让你会心一笑！😄 如果想要听更多笑话，尽管告诉我哦！"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:14.549"
},
{
"id":"MXbU8iV25Sn6RRkyGMKFGN",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"call_f980d2ddcad24e8588e156",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:19.701"
},
{
"id":"3nm3K3D3vuEAwxCwf9UAba",
"name":"ChatBot",
"role":"assistant",
"content":"对的，那个笑话是这样的：为什么电脑经常生病？因为它的窗户（Windows）总是开着啊！这是一个利用了双关的小幽默，把电脑的操作系统Windows比作了真的窗户。希望这个笑话能让你会心一笑！😄 如果想要听更多笑话，尽管告诉我哦！",
"metadata":null,
"timestamp":"2025-11-02 15:32:19.701"
},
{
"id":"d5PL3Pm9bna2hxV9tL4MUk",
"name":"owen",
"role":"user",
"content":"你好",
"metadata":null,
"timestamp":"2025-11-02 15:32:43.508"
},
{
"id":"aStLHJye8hpfko5b5EpJK6",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"id":"SXXNZtumZSDXznnWQqdU7E",
"type":"tool_use",
"name":"generate_response",
"input":{
"response":"你好！我们又见面了，有什么好玩的事情想和我分享吗？或者你想要再来点笑话？😉 如果需要帮助也尽管告诉我哦！"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:44.137"
},
{
"id":"HGYQqjS3qhPvosZasTQAok",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"SXXNZtumZSDXznnWQqdU7E",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:45.743"
},
{
"id":"AfXBKk6ZiWaukfQkDTW7EV",
"name":"ChatBot",
"role":"assistant",
"content":"你好！我们又见面了，有什么好玩的事情想和我分享吗？或者你想要再来点笑话？😉 如果需要帮助也尽管告诉我哦！",
"metadata":null,
"timestamp":"2025-11-02 15:32:45.743"
},
{
"id":"8G48SBccEnv5ZthsKo7cZs",
"name":"owen",
"role":"user",
"content":"讲个笑话",
"metadata":null,
"timestamp":"2025-11-02 15:32:48.309"
},
{
"id":"2R8V5dRwuBR6EZDGdfmjZ8",
"name":"ChatBot",
"role":"assistant",
"content":[
{
"type":"tool_use",
"id":"call_e011e3a692da4d9db22c69",
"name":"generate_response",
"input":{
"response":"好的，那我再给你讲一个笑话吧！\n\n为什么26个字母只剩下25个了？因为Q被拴住了（queue，队列，听起来像‘cue’，提示）！哈哈，这个有点冷门，希望你喜欢～ 😄"
}
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:49.598"
},
{
"id":"G6PDu2wFEDqWFS6bHiVyEu",
"name":"system",
"role":"system",
"content":[
{
"type":"tool_result",
"id":"call_e011e3a692da4d9db22c69",
"name":"generate_response",
"output":[
{
"type":"text",
"text":"Successfully generated response."
}
]
}
],
"metadata":null,
"timestamp":"2025-11-02 15:32:52.228"
},
{
"id":"QxrVbS8r8tsVFLn8fxHehH",
"name":"ChatBot",
"role":"assistant",
"content":"好的，那我再给你讲一个笑话吧！\n\n为什么26个字母只剩下25个了？因为Q被拴住了（queue，队列，听起来像‘cue’，提示）！哈哈，这个有点冷门，希望你喜欢～ 😄",
"metadata":null,
"timestamp":"2025-11-02 15:32:52.228"
}
]
},
"toolkit":{
"active_groups":[
]
},
"_reasoning_hint_msgs":{
"content":[
]
},
"name":"ChatBot",
"_sys_prompt":"幽默的助手，爱开玩笑"
}
}
```