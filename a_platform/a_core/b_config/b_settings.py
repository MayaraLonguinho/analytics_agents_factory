from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    
    # LLM Providers
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-1.5-pro"
    
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20240620"

    class Config:
        env_file = ".env"

settings = Settings()
