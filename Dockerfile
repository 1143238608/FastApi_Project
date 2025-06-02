FROM python:3.10-slim

# 使用绝对路径
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -U magic-pdf[full] --extra-index-url https://wheels.myhloli.com -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制整个app目录内容
COPY ./app .

# 专门创建env文件存放目录
RUN mkdir -p /config && \
    touch /config/.env && \
    chmod 644 /config/.env

# 复制.env文件到专门目录（安全考虑）
COPY .env /config/.env

EXPOSE 8000

# 启动时指定环境变量文件位置
CMD ["sh", "-c", "export $(grep -v '^#' /config/.env | xargs) && uvicorn main:app --host 0.0.0.0 --port 8000"]