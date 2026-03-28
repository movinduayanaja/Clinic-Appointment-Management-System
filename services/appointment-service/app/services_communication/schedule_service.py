import httpx
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SCHEDULE_SERVICE_URL: str | None = None
    SERVICE_NAME: str | None = None
    PORT: int | None = None
    DATABASE_URL: str | None = None

    model_config = {
        "extra": "ignore",
        "env_file": ".env",
    }


settings = Settings()


async def fetch_schedule(schedule_id: int):
    url = f"{settings.SCHEDULE_SERVICE_URL}/schedules/{schedule_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
        except Exception:
            return None
    return None