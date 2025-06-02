import json
import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory,ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
import os
from operator import itemgetter
from dotenv import load_dotenv

# 设置环境变量（DeepSeek API 密钥）
load_dotenv('D:\code\project\FastApi_Project\.env')
os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
prompt = ChatPromptTemplate.from_messages(
    [
        ('system',"你是高级逆向工程师，请你根据对应的上下文回复用户问题"),
        MessagesPlaceholder("history"),
        ("human","{query}")
    ]
)

llm = ChatDeepSeek(
    model="deepseek-chat",  # 指定 DeepSeek 模型名称  deepseek-reasoner  deepseek-chat
    temperature=0.7,  # 可选：设置生成的随机性
    max_tokens=200,  # 可选：设置最大输出长度
    timeout=None,  # 可选：设置请求超时时间
    max_retries=2  # 可选：设置最大重试次数
)
memory = ConversationBufferMemory(return_messages=True,input_key="query")

chain = RunnablePassthrough.assign(
    history = RunnableLambda(memory.load_memory_variables) | itemgetter("history")
) | prompt | llm | StrOutputParser()

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

async def stream_generator(response):
    output = ""
    for chunk in response:
        output += chunk
        print(chunk,flush=True,end="")
        yield output
@router.get("/events")
async def get_events():
    return EventSourceResponse(event_generator())


@router.post("/events")
async def post_events():
    return EventSourceResponse(event_generator())

@router.get("/chat")
async def get_chat():

    # 使用异步调用（如果支持）
    # response = await llm.ainvoke("你好")  # 注意：必须是 async def 和 await
    # return {"response": response.content}
    chain_input = {"query": '你好'}
    response = chain.stream(chain_input)

    return EventSourceResponse(stream_generator(response))