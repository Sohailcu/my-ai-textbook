from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql+asyncpg://user:password@localhost/dbname"
    
    # Qdrant settings
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None
    
    # API settings
    api_prefix: str = "/api"
    debug: bool = False
    
    # JWT settings
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI settings
    openai_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()