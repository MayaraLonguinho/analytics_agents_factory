"""
g_configuration/a_settings.py
=============================
Single Source of Truth (SSOT) para a configuração operacional externa do AAF.
Gerencia variáveis de ambiente e parâmetros operacionais via Pydantic Settings.

Princípios arquiteturais:
1. Fornece VALORES configuráveis; consumidores implementam COMPORTAMENTO e POLÍTICAS.
2. Nenhum secret é hardcoded; leitura segura a partir de variáveis de ambiente e .env.
3. Não implementa lógica de negócios, decisões de arquitetura, gates ou orquestração.
"""
from pathlib import Path
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolução canônica da raiz do repositório e do arquivo .env
REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = REPO_ROOT / ".env"


class AAFSettings(BaseSettings):
    """
    Configurações operacionais da plataforma Analytics Agents Factory (AAF).
    """

    # --- LLM Gateway Settings ---
    llm_provider: str = Field(
        default="openai",
        description="Provedor primário de LLM (ex: 'openai', 'anthropic', 'gemini')."
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="Modelo de referência padrão para geração analítica e agentes."
    )
    openai_api_key: str = Field(
        default="",
        description="Chave de autenticação da API OpenAI."
    )
    anthropic_api_key: str = Field(
        default="",
        description="Chave de autenticação da API Anthropic (quando habilitada)."
    )
    gemini_api_key: str = Field(
        default="",
        description="Chave de autenticação da API Google Gemini (quando habilitada)."
    )

    # --- Paths Operacionais ---
    project_output_dir: str = Field(
        default=str(REPO_ROOT / "e_generated_projects"),
        description="Caminho raiz canônico para materialização física dos projetos fabricados."
    )

    # --- Runtime Configuration ---
    command_timeout_seconds: float = Field(
        default=120.0,
        ge=1.0,
        description="Tempo limite padrão em segundos para execução de comandos em subprocesso no Runtime."
    )

    # --- Repair & Recovery Configuration ---
    max_repair_attempts: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Número máximo de tentativas locais de auto-recuperação antes de escalonamento ou reclassificação da falha."
    )

    # --- Logging & Telemetria ---
    log_level: str = Field(
        default="INFO",
        description="Nível de severidade para logging da plataforma (DEBUG, INFO, WARNING, ERROR)."
    )

    @field_validator("llm_provider", mode="before")
    @classmethod
    def normalize_provider(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            return v.strip().lower()
        return "openai"

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, v: Optional[str]) -> str:
        if isinstance(v, str):
            return v.strip().upper()
        return "INFO"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH) if ENV_FILE_PATH.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


# Alias canônico
Settings = AAFSettings


def get_settings() -> AAFSettings:
    """Retorna uma nova instância das configurações operacionais."""
    return AAFSettings()


# Singleton global para compatibilidade com consumidores existentes
settings = AAFSettings()
