from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    ENVIRONMENT: str = "production"
    CORS_ORIGINS: List[str] = ["*"] # Mobile apps don't typically enforce CORS, but this is useful if testing on Flutter Web
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
