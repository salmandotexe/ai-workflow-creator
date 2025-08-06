from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    MONGODB_URL: str = "mongodb://mongo:27017/"
    CELERY_BACKEND_DB: str = "celery_results"

    class Config:
        env_file = ".env"

settings = Settings()