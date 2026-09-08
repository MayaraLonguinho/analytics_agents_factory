"""
Configuração do contexto do Brain.

Mantém as configurações relacionadas ao contexto, histórico
de conversação e integração com memória de longo prazo.
"""

from copy import deepcopy
import os
from typing import Any, Dict, Optional

import yaml


class BrainConfig:
    """
    Configuração central do contexto do Brain.
    """

    DEFAULT_CONFIG = {
        "module": {
            "name": "brain",
            "version": "1.0.0",
            "log_level": "INFO",
        },
        "brain": {
            "max_conversation_history": 10,
            "context_window": 4096,
            "enable_long_term_memory": True,
        },
        "memory": {
            "backend": "sqlite",
            "connection_string": "",
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config = deepcopy(self.DEFAULT_CONFIG)

        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)

        self._validate_config()

    def _load_from_file(self, config_path: str) -> None:
        """
        Carrega configuração a partir de um arquivo YAML.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                file_config = yaml.safe_load(file) or {}

            self._merge_config(
                self.config,
                file_config,
            )

        except Exception as error:
            raise ValueError(
                f"Erro ao carregar configuração: {error}"
            ) from error

    def _merge_config(
        self,
        base: Dict[str, Any],
        override: Dict[str, Any],
    ) -> None:
        """
        Mescla configurações mantendo estruturas aninhadas.
        """
        for key, value in override.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                self._merge_config(
                    base[key],
                    value,
                )
            else:
                base[key] = value

    def _validate_config(self) -> None:
        """
        Valida as configurações mínimas do Brain.
        """
        max_history = (
            self.config
            .get("brain", {})
            .get("max_conversation_history")
        )

        if max_history is None:
            raise ValueError(
                "max_conversation_history é obrigatório."
            )

        if max_history <= 0:
            raise ValueError(
                "max_conversation_history deve ser positivo."
            )

    def get(
        self,
        section: str,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Recupera uma configuração específica.
        """
        return self.config.get(
            section,
            {},
        ).get(
            key,
            default,
        )

    def get_all(self) -> Dict[str, Any]:
        """
        Retorna uma cópia completa da configuração.
        """
        return deepcopy(self.config)