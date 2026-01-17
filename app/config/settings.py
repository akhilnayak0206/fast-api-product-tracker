from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Product Tracker API"
    app_version: str = "1.0.0"
    app_description: str = "A simple API for managing products"
    
    # Database settings (will be overridden by DATABASE_URL env var if set)
    database_url: str = "postgresql://postgres:your_password@localhost:5432/your_database"
    
    # CORS settings
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    # Environment settings
    environment: str = "development"
    debug: bool = True
    
    # AI settings
    api_kaiey: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()
