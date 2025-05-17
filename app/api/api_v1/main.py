import json
import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter
from app.services import chat
router = APIRouter()


@router.get("/user")
async def root():
    return {"Hello": "World"}


async def event_generator():
    count = 0
    while True:
        await asyncio.sleep(1)
        count += 1
        data = {"count": count}
        yield json.dumps(data)


@router.get("/events")
async def get_events():
    return EventSourceResponse(event_generator())


@router.post("/events")
async def post_events():
    return EventSourceResponse(event_generator())

@router.post("/chat")
async def get_chat():
    from langchain_deepseek import ChatDeepSeek
    import os
    # 设置环境变量（DeepSeek API 密钥）
    os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
    llm = ChatDeepSeek(
        model="deepseek-chat",  # 指定 DeepSeek 模型名称  deepseek-reasoner  deepseek-chat
        temperature=0.7,  # 可选：设置生成的随机性
        max_tokens=200,  # 可选：设置最大输出长度
        timeout=None,  # 可选：设置请求超时时间
        max_retries=2  # 可选：设置最大重试次数
    )

    return llm.invoke('你好')
