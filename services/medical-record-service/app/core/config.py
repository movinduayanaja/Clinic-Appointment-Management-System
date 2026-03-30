from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVICE_NAME: str | None = "medical-record-service"
    PORT: int | None = 8005
    DOCTOR_SERVICE_URL: str | None = None
    PATIENT_SERVICE_URL: str | None = None

    model_config = {
        "extra": "ignore",
        "env_file": ".env"
    }

settings = Settings()
