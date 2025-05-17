# -*- coding: utf-8 -*-
"""
    @Time   : 2025/5/17 11:11
    @Author : mxy
"""


from langchain_deepseek import ChatDeepSeek
import os

# 设置环境变量（DeepSeek API 密钥）
os.environ["DEEPSEEK_API_KEY"] = "sk-77c7047241e7436490f08b5abf391a6a"
llm = ChatDeepSeek(
    model="deepseek-chat",  # 指定 DeepSeek 模型名称  deepseek-reasoner  deepseek-chat
    temperature=0.7,  # 可选：设置生成的随机性
    max_tokens=200,  # 可选：设置最大输出长度
    timeout=None,  # 可选：设置请求超时时间
    max_retries=2  # 可选：设置最大重试次数
)

response = llm.invoke('你好')
print(response)