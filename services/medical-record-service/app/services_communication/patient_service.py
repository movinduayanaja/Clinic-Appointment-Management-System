import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def fetch_patient_name(patient_id: int) -> str | None:
    if not settings.PATIENT_SERVICE_URL:
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.PATIENT_SERVICE_URL}/api/v1/patients/{patient_id}")
            if response.status_code == 200:
                data = response.json()
                return data.get("full_name")
    except Exception as e:
        logger.error(f"Error fetching patient name: {e}")
    
    return None
