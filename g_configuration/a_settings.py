from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class AAFSettings(BaseSettings):
    # LLM Settings
    llm_provider: str = Field(default="openai", description="Provedor de LLM primário (ex: openai)")
    llm_model: str = Field(default="gpt-4o-mini", description="Modelo LLM a ser utilizado")
    openai_api_key: str = Field(default="", description="Chave de API OpenAI")
    
    # Paths
    project_output_dir: str = Field(
        default=os.path.join(os.getcwd(), "e_generated_projects"), 
        description="Diretório raiz para materialização de projetos"
    )
    
    # Runtime Config
    max_repair_attempts: int = Field(default=3, description="Tentativas máximas do Repair Loop")
    
    # Environment Setup
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instância Singleton global
settings = AAFSettings()
