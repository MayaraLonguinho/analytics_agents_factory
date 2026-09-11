"""
Configuração do Orchestrator Agent
Carrega e valida configurações do agente
"""

import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path


class OrchestratorConfig:
    """
    Classe de configuração do Orchestrator Agent.
    Gerencia carregamento e validação de configurações.
    """
    
    DEFAULT_CONFIG = {
        "agent": {
            "name": "orchestrator_agent",
            "version": "1.0.0",
            "log_level": "INFO"
        },
        "orchestration": {
            "max_concurrent_agents": 5,
            "timeout_per_agent": 300,
            "retry_attempts": 3,
            "retry_delay": 5
        },
        "workflow": {
            "default_sequence": [
                "architecture_agent",
                "backend_agent",
                "frontend_agent",
                "database_agent",
                "etl_agent",
                "analytics_agent",
                "testing_agent",
                "documentation_agent",
                "deployment_agent"
            ]
        },
        "error_handling": {
            "continue_on_error": False,
            "rollback_on_failure": True,
            "notify_on_failure": True
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa a configuração.
        
        Args:
            config_path: Caminho opcional para arquivo de configuração YAML
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)
        
        self._load_from_environment()
        self._validate_config()
    
    def _load_from_file(self, config_path: str) -> None:
        """
        Carrega configuração de arquivo YAML.
        
        Args:
            config_path: Caminho do arquivo de configuração
        """
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)
                self._merge_config(self.config, file_config)
        except Exception as e:
            raise ValueError(f"Erro ao carregar configuração de {config_path}: {e}")
    
    def _load_from_environment(self) -> None:
        """
        Sobrescreve configurações com variáveis de ambiente.
        """
        env_mappings = {
            "ORCHESTRATOR_MAX_CONCURRENT": ("orchestration", "max_concurrent_agents"),
            "ORCHESTRATOR_TIMEOUT": ("orchestration", "timeout_per_agent"),
            "ORCHESTRATOR_RETRY_ATTEMPTS": ("orchestration", "retry_attempts"),
            "ORCHESTRATOR_LOG_LEVEL": ("agent", "log_level"),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self.config[section][key] = self._convert_type(value)
    
    def _convert_type(self, value: str) -> Any:
        """
        Converte string para tipo apropriado.
        
        Args:
            value: Valor string a converter
            
        Returns:
            Valor convertido para tipo apropriado
        """
        # Tentar converter para int
        try:
            return int(value)
        except ValueError:
            pass
        
        # Tentar converter para bool
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # Retornar como string
        return value
    
    def _merge_config(self, base: Dict, override: Dict) -> None:
        """
        Mescla recursivamente dicionários de configuração.
        
        Args:
            base: Dicionário base
            override: Dicionário de sobrescrita
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _validate_config(self) -> None:
        """
        Valida a configuração carregada.
        Levanta ValueError se inválida.
        """
        # Validar orchestration
        orch = self.config["orchestration"]
        if orch["max_concurrent_agents"] < 1 or orch["max_concurrent_agents"] > 10:
            raise ValueError("max_concurrent_agents deve estar entre 1 e 10")
        
        if orch["timeout_per_agent"] < 60:
            raise ValueError("timeout_per_agent deve ser maior que 60 segundos")
        
        if orch["retry_attempts"] < 0 or orch["retry_attempts"] > 10:
            raise ValueError("retry_attempts deve estar entre 0 e 10")
        
        # Validar workflow
        if not self.config["workflow"]["default_sequence"]:
            raise ValueError("default_sequence não pode estar vazio")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtém um valor de configuração específico.
        
        Args:
            section: Seção da configuração
            key: Chave dentro da seção
            default: Valor padrão se não encontrado
            
        Returns:
            Valor da configuração ou default
        """
        return self.config.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Obtém uma seção completa da configuração.
        
        Args:
            section: Nome da seção
            
        Returns:
            Dicionário com a seção da configuração
        """
        return self.config.get(section, {})
    
    def get_all(self) -> Dict[str, Any]:
        """
        Retorna toda a configuração.
        
        Returns:
            Dicionário completo da configuração
        """
        return self.config.copy()
