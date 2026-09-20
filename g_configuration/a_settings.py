"""
g_configuration/a_settings.py
=============================

Single Source of Truth (SSOT) para a configuração operacional externa do AAF.

Gerencia variáveis de ambiente e parâmetros operacionais via Pydantic Settings.

Princípios arquiteturais:
1. Fornece VALORES configuráveis; consumidores implementam COMPORTAMENTO e POLÍTICAS.
2. Nenhum secret é hardcoded; credenciais são obtidas de variáveis de ambiente e/ou .env.
3. Não implementa lógica de negócio, decisões de arquitetura, gates ou orquestração.
4. Valores explicitamente fornecidos e inválidos geram erro; não há fallback silencioso.
5. Defaults declarados são aplicados somente quando a configuração correspondente é omitida.
"""

from pathlib import Path
from typing import Any, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------------------------
# Repository environment
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = REPO_ROOT / ".env"


# ---------------------------------------------------------------------------
# LLM configuration contract
# ---------------------------------------------------------------------------

SUPPORTED_LLM_PROVIDERS: frozenset[str] = frozenset(
    {
        "openai",
        "anthropic",
        "gemini",
    }
)


class AAFSettings(BaseSettings):
    """
    Configurações operacionais externas do Analytics Agents Factory (AAF).

    Esta classe fornece somente valores configuráveis.
    A interpretação e o comportamento associados a esses valores pertencem
    aos respectivos consumidores.
    """

    # -----------------------------------------------------------------------
    # LLM Gateway
    # -----------------------------------------------------------------------

    llm_provider: Literal["openai", "anthropic", "gemini"] = Field(
        default="openai",
        description=(
            "Provedor padrão de LLM suportado pelo AAF: "
            "'openai', 'anthropic' ou 'gemini'."
        ),
    )

    llm_model: str = Field(
        default="gpt-4o-mini",
        min_length=1,
        description="Modelo padrão de LLM utilizado pelos consumidores.",
    )

    openai_api_key: str = Field(
        default="",
        description="Chave de autenticação da API OpenAI.",
    )

    anthropic_api_key: str = Field(
        default="",
        description="Chave de autenticação da API Anthropic.",
    )

    gemini_api_key: str = Field(
        default="",
        description="Chave de autenticação da API Google Gemini.",
    )

    # -----------------------------------------------------------------------
    # Runtime
    # -----------------------------------------------------------------------

    command_timeout_seconds: float = Field(
        default=120.0,
        ge=1.0,
        description=(
            "Tempo limite operacional, em segundos, disponibilizado aos "
            "consumidores responsáveis pela execução de subprocessos."
        ),
    )

    # -----------------------------------------------------------------------
    # Repair & Recovery
    # -----------------------------------------------------------------------

    max_repair_attempts: int = Field(
        default=3,
        ge=1,
        le=10,
        description=(
            "Número máximo de tentativas locais de auto-recuperação antes "
            "de escalonamento ou reclassificação da falha."
        ),
    )

    # -----------------------------------------------------------------------
    # Validators
    # -----------------------------------------------------------------------

    @field_validator("llm_provider", mode="before")
    @classmethod
    def validate_llm_provider(cls, value: Any) -> str:
        """
        Normaliza e valida estritamente o provedor de LLM.

        Regras:
        - quando o campo é omitido, o default declarado no Field é utilizado;
        - quando fornecido, o valor deve obrigatoriamente ser uma string;
        - strings são normalizadas com strip() e lower();
        - somente provedores oficialmente suportados são aceitos;
        - valores inválidos, incluindo None explícito, geram erro;
        - nenhum valor inválido é convertido silenciosamente para o default.
        """

        if not isinstance(value, str):
            raise ValueError(
                "llm_provider deve ser uma string válida; "
                f"recebido: {type(value).__name__}"
            )

        normalized = value.strip().lower()

        if normalized not in SUPPORTED_LLM_PROVIDERS:
            supported = ", ".join(sorted(SUPPORTED_LLM_PROVIDERS))
            raise ValueError(
                f"Provedor LLM inválido: {value!r}. "
                f"Provedores suportados: {supported}."
            )

        return normalized

    # -----------------------------------------------------------------------
    # Pydantic Settings
    # -----------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

# Alias preservado para compatibilidade com consumidores existentes.
Settings = AAFSettings


def get_settings() -> AAFSettings:
    """
    Retorna uma nova instância das configurações operacionais do AAF.
    """

    return AAFSettings()


# Instância global preservada para compatibilidade com consumidores existentes.
settings = AAFSettings()