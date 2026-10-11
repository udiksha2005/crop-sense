from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Crop Sense"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./cropsense_app.db"
    MODEL_PATH: str = "crop_sense_model.pth"
    YOLO_MODEL_PATH: str = "yolov8n.pt"
    CONFIDENCE_THRESHOLD: float = 60.0
    UPLOAD_DIRECTORY: str = "backend/uploads"
    MAX_UPLOAD_SIZE: int = 5242880
    SECRET_KEY: str = "your_secret_key_here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

@lru_cache()
def get_settings() -> Settings:
    return Settings()
