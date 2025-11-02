from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit, execute_python_code
from agentscope.session import JSONSession
from agentscope.message import Msg
import os 

app = FastAPI(title="Simple SSE API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/stream")
async def stream(username,query):
    # 会话管理
    session_mgr=JSONSession(save_dir='./sessions')
    
    # 智能体
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    agent = ReActAgent(
        name="ChatBot",
        sys_prompt="幽默的助手，爱开玩笑",
        model=OpenAIChatModel(
            client_args={
                'base_url':'https://dashscope.aliyuncs.com/compatible-mode/v1',
            },
            model_name="qwen-max",
            api_key=os.environ.get('API_KEY'),
            stream=True,
        ),
        memory=InMemoryMemory(),
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
    )
    agent.set_console_output_enabled(False)
    
    # 清理早期记忆
    async def mem_chunk(agent,kwargs,output):
        while await agent.memory.size()>50:
            await agent.memory.delete(0)
    agent.register_instance_hook(hook_type="post_reply",hook_name="mem_trunc", hook=mem_chunk)
    
    # 加载状态
    await session_mgr.load_session_state(session_id=username,allow_not_exist=True,agent=agent)
 
    sse_queue=asyncio.Queue()
    
    # 应答放入队列
    async def stream_collect(agent,kwargs):
        response=''
        for block in kwargs['msg'].get_content_blocks('text'):
            response=block['text']
        if response:
            await sse_queue.put(response)
    agent.register_instance_hook(hook_type="pre_print",hook_name="sse",hook=stream_collect)
        
    # 应答回复客户端
    async def stream_response():
        while True:
            msg=await sse_queue.get()
            if msg is None:
                break
            chunk=json.dumps({"message": msg})
            yield 'data: %s\n\n' % chunk
    
    # 异步执行agent
    async def execute_agent():
        final_msg=None
        try:
            input_msg=Msg(name=username,content=query,role='user')
            final_msg=await agent(input_msg)
        except Exception as e:
            print(e)
        await session_mgr.save_session_state(session_id=username,agent=agent)
        await sse_queue.put(None)
        print(f'Username:{username} Query:{query} Answer:{final_msg}')
    asyncio.create_task(execute_agent())
    
    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)