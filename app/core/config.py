class Settings():
    PROJECT_NAME: str = "My FastAPI Project"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"


settings = Settings()
