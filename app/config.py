import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SubLedger - SaaS Subscription & Billing System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./subledger.db"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
