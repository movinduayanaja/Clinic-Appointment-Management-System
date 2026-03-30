from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVICE_NAME: str
    PORT: int

    class Config:
        env_file = ".env"

settings = Settings()