from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = "patient-service"
    port: int = 8001
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()