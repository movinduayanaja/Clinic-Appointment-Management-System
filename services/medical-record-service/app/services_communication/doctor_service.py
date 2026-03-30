import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def fetch_doctor_name(doctor_id: int) -> str | None:
    if not settings.DOCTOR_SERVICE_URL:
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.DOCTOR_SERVICE_URL}/api/v1/doctors/{doctor_id}")
            if response.status_code == 200:
                data = response.json()
                return data.get("full_name")
    except Exception as e:
        logger.error(f"Error fetching doctor name: {e}")
    
    return None
