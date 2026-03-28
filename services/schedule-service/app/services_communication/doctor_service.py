import httpx
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DOCTOR_SERVICE_URL: str | None = None
    SERVICE_NAME: str | None = None      # ✅ allow SERVICE_NAME
    PORT: int | None = None              # ✅ allow PORT
    DATABASE_URL: str | None = None      # ✅ allow DATABASE_URL

    model_config = {
        "extra": "ignore",               # ✅ ignore extra .env keys
        "env_file": ".env",
    }

settings = Settings()

async def fetch_doctor_name(doctor_id: int) -> str | None:
    url = f"{settings.DOCTOR_SERVICE_URL}/doctors/{doctor_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                return data["full_name"]
        except Exception:
            return None
    return None