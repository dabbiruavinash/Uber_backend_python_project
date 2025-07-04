# Configuration Management

import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SMS_PROVIDER_URL: str = os.getenv("SMS_PROVIDER_URL", "")
    SMS_API_KEY: str = os.getenv("SMS_API_KEY", "")
    
    # India-specific configurations
    DEFAULT_CURRENCY: str = "INR"
    DEFAULT_TIMEZONE: str = "Asia/Kolkata"
    SUPPORTED_LANGUAGES: list = ["en", "hi", "ta", "te", "kn", "ml", "bn", "mr"]
    
    class Config:
        env_file = ".env"

settings = Settings()