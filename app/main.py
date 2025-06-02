from pathlib import Path

from fastapi import FastAPI
import dotenv
from fastapi.middleware.cors import CORSMiddleware
from api.api_v1 import api
from dotenv import load_dotenv

app = FastAPI()

# 1.将env加载到环境变量中
# dotenv.load_dotenv()
# 加载环境变量docker 环境
env_path = Path('/config') / '.env'
load_dotenv(dotenv_path=env_path)
# 设置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 将主路由器添加到应用中
app.include_router(api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
