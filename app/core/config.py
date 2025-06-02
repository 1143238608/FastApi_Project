from pathlib import Path

class Settings():
    PROJECT_NAME: str = "My FastAPI Project"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        env_path = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = "utf-8"  # 处理中文等特殊字符

settings = Settings()
print(settings.Config.env_path)