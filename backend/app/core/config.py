from pydantic_settings import BaseSettings
from pathlib import Path
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    MONGODB_URL: str = "mongodb://mongo:27017/"
    CELERY_BACKEND_DB: str = "celery_results"
    STORAGE_DIR: Path = Path("/shared/screenshots")

    class Config:
        env_file = ".env"

settings = Settings()

@lru_cache()
def get_settings() -> Settings:
    return Settings()