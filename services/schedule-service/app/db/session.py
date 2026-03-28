from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVICE_NAME: str | None = None   # ✅ allow SERVICE_NAME
    PORT: int | None = None           # ✅ allow PORT
    DOCTOR_SERVICE_URL: str | None = None  # ✅ allow doctor service URL

    model_config = {
        "extra": "ignore",            # ✅ ignore extra .env values
        "env_file": ".env"
    }

settings = Settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()