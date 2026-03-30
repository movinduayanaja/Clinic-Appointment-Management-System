from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str | None = None
    PORT: int | None = None
    DATABASE_URL: str

    PATIENT_SERVICE_URL: str
    DOCTOR_SERVICE_URL: str
    SCHEDULE_SERVICE_URL: str

    model_config = {
        "extra": "ignore",
        "env_file": ".env",
    }


settings = Settings()