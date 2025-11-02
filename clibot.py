from agentscope.agent import ReActAgent, UserAgent
from agentscope.model import OpenAIChatModel
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit, execute_python_code, execute_shell_command
import asyncio
import os 

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    agent = ReActAgent(
        name="Friday",
        sys_prompt="You're a helpful assistant named Friday.",
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
    
    sse_queue=asyncio.Queue()
    def sse_queue(agent,kwargs):
        print('sse_response',kwargs)
        sse_queue.put_nowait(kwargs)
    agent.register_instance_hook(hook_type="pre_print", hook_name="sse", hook=sse_response)

    user = UserAgent(name="user")

    msg = None
    while True:
        msg = await agent(msg)
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break

#agentscope.init(project='main',studio_url='http://localhost:3000')
asyncio.run(main())