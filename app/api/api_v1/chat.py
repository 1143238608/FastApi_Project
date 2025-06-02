# -*- coding: utf-8 -*-
"""
    @Time   : 2025/6/1 16:01
    @Author : mxy
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
import os
from fastapi.responses import StreamingResponse
from fastapi import APIRouter
router = APIRouter()

@router.api_route("/",methods=["GET"])
async def chat(query: str):
    # 设置环境变量（DeepSeek API 密钥）
    # os.environ["DEEPSEEK_API_KEY"] = "sk-77c7047241e7436490f08b5abf391a6a"
    os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")


    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.7,
        max_tokens=1000,
        timeout=None,
        max_retries=2
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ('system', "你是一个PDF合同文本提取大师，你可以根据问题中的描述提取对应的信息"),
            ("human", "{query}")
        ]
    )
    chain = prompt | llm
    # 创建生成器函数来流式传输响应
    async def generate():
        for chunk in chain.stream(query):
            content = chunk.content
            print(content)
            yield content

    return StreamingResponse(generate(), media_type="text/plain")

@router.get("/fast/{query}")
async def chatFastGpt(query: str):
    pass
