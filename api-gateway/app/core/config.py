from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DOCTOR_SERVICE_URL: str
    SCHEDULE_SERVICE_URL: str
    PATIENT_SERVICE_URL: str   
    APPOINTMENT_SERVICE_URL: str 

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()